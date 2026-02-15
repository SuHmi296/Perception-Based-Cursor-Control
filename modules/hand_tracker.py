import cv2

try:
    import mediapipe as mp
except Exception as exc:
    raise RuntimeError("MediaPipe is not installed correctly.") from exc


def _get_hands_module():
    if hasattr(mp, "solutions") and hasattr(mp.solutions, "hands"):
        return mp.solutions.hands
    raise RuntimeError(
        "This project requires MediaPipe Solutions API (mp.solutions.hands). "
        "Install a compatible version: pip install mediapipe==0.10.14"
    )


class HandTracker:
    def __init__(self, min_detection_confidence: float, min_tracking_confidence: float):
        self._mp_hands = _get_hands_module()
        self._hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def process(self, frame_bgr):
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        result = self._hands.process(rgb)
        if not result.multi_hand_landmarks:
            return None, None

        hand_landmarks = result.multi_hand_landmarks[0]
        handedness = None
        if result.multi_handedness:
            handedness = result.multi_handedness[0].classification[0].label
        return hand_landmarks, handedness

    def close(self) -> None:
        self._hands.close()
