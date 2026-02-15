import time
from typing import Dict, Optional, Tuple

from utils.math_utils import distance_2d


TIP_IDS = {
    "thumb": 4,
    "index": 8,
    "middle": 12,
    "ring": 16,
    "pinky": 20,
}

PIP_IDS = {
    "index": 6,
    "middle": 10,
    "ring": 14,
    "pinky": 18,
}


class GestureController:
    def __init__(self, pinch_threshold: float, hold_seconds: float, click_cooldown_seconds: float, scroll_gain: float):
        self.pinch_threshold = pinch_threshold
        self.hold_seconds = hold_seconds
        self.click_cooldown_seconds = click_cooldown_seconds
        self.scroll_gain = scroll_gain

        self._active_gesture: Optional[str] = None
        self._gesture_started_at: float = 0.0
        self._last_click_at: float = 0.0

        self._dragging = False
        self._previous_index_y = None

    @staticmethod
    def _finger_up(hand_landmarks, tip_idx: int, pip_idx: int) -> bool:
        return hand_landmarks.landmark[tip_idx].y < hand_landmarks.landmark[pip_idx].y

    @staticmethod
    def _point(hand_landmarks, idx: int) -> Tuple[float, float]:
        lm = hand_landmarks.landmark[idx]
        return lm.x, lm.y

    def _update_hold_timer(self, gesture: Optional[str], now: float) -> float:
        if gesture != self._active_gesture:
            self._active_gesture = gesture
            self._gesture_started_at = now
        return now - self._gesture_started_at

    def detect(self, hand_landmarks, now: Optional[float] = None) -> Dict[str, object]:
        now = now if now is not None else time.time()

        result = {
            "gesture": "none",
            "paused": False,
            "pen_active": False,
            "pen_point": None,
            "click": False,
            "drag_down": False,
            "drag_up": False,
            "scroll_mode": False,
            "scroll_delta": 0,
            "dragging": self._dragging,
        }

        if hand_landmarks is None:
            held = self._update_hold_timer(None, now)
            _ = held
            if self._dragging:
                result["drag_up"] = True
                self._dragging = False
            self._previous_index_y = None
            result["dragging"] = self._dragging
            return result

        index_up = self._finger_up(hand_landmarks, TIP_IDS["index"], PIP_IDS["index"])
        middle_up = self._finger_up(hand_landmarks, TIP_IDS["middle"], PIP_IDS["middle"])
        ring_up = self._finger_up(hand_landmarks, TIP_IDS["ring"], PIP_IDS["ring"])
        pinky_up = self._finger_up(hand_landmarks, TIP_IDS["pinky"], PIP_IDS["pinky"])

        fingers_up_count = sum([index_up, middle_up, ring_up, pinky_up])

        thumb = self._point(hand_landmarks, TIP_IDS["thumb"])
        index = self._point(hand_landmarks, TIP_IDS["index"])
        pinch_distance = distance_2d(thumb, index)

        raw_gesture = "none"
        if pinch_distance < self.pinch_threshold:
            raw_gesture = "pinch"
        elif index_up and middle_up and not ring_up and not pinky_up:
            raw_gesture = "two_fingers"
        elif fingers_up_count == 0:
            raw_gesture = "fist"
        elif fingers_up_count >= 4:
            raw_gesture = "open_palm"

        held_for = self._update_hold_timer(raw_gesture, now)
        stable = held_for >= self.hold_seconds
        result["gesture"] = raw_gesture
        result["paused"] = raw_gesture == "open_palm"

        if raw_gesture == "pinch" and stable:
            if now - self._last_click_at >= self.click_cooldown_seconds:
                result["click"] = True
                self._last_click_at = now

        if raw_gesture == "fist" and stable:
            if not self._dragging:
                result["drag_down"] = True
                self._dragging = True

        if self._dragging and raw_gesture != "fist":
            result["drag_up"] = True
            self._dragging = False

        if raw_gesture == "two_fingers" and stable:
            result["scroll_mode"] = True
            index_y = hand_landmarks.landmark[TIP_IDS["index"]].y
            if self._previous_index_y is not None:
                delta = self._previous_index_y - index_y
                result["scroll_delta"] = int(delta * self.scroll_gain * 100)
            self._previous_index_y = index_y
        else:
            self._previous_index_y = None

        if raw_gesture not in {"open_palm", "fist"} and not result["scroll_mode"]:
            result["pen_active"] = True
            result["pen_point"] = index

        result["dragging"] = self._dragging
        return result
