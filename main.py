import time

import cv2

from config import CFG
from modules.camera import CameraStream
from modules.cursor_controller import CursorController
from modules.gesture_controller import GestureController
from modules.hand_tracker import HandTracker
from modules.smoothing import CursorSmoother


def draw_status(frame, fps: float, tracking: bool, gesture: str, dragging: bool, paused: bool):
    if not tracking:
        status_text = "Hand Lost"
        status_color = (0, 0, 255)
    elif paused:
        status_text = "Paused (Touchpad Enabled)"
        status_color = (0, 220, 255)
    else:
        status_text = "Pen Active"
        status_color = (0, 200, 0)

    cv2.rectangle(frame, (10, 10), (470, 130), (20, 20, 20), -1)
    cv2.putText(frame, f"FPS: {fps:.1f}", (20, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 220, 255), 2)
    cv2.putText(frame, f"Status: {status_text}", (20, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
    cv2.putText(frame, f"Gesture: {gesture}", (20, 86), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 0), 2)
    cv2.putText(frame, f"Drag: {'ON' if dragging else 'OFF'}", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


def main():
    camera = CameraStream(CFG.camera_index, CFG.frame_width, CFG.frame_height)
    hand_tracker = HandTracker(CFG.hand_min_detection_confidence, CFG.hand_min_tracking_confidence)

    cursor = CursorController(
        CFG.cursor_sensitivity_x,
        CFG.cursor_sensitivity_y,
        invert_x=CFG.invert_x,
        invert_y=CFG.invert_y,
        max_cursor_step_px=CFG.max_cursor_step_px,
        pen_active_margin_x=CFG.pen_active_margin_x,
        pen_active_margin_y=CFG.pen_active_margin_y,
    )
    smoother = CursorSmoother(alpha=CFG.smoothing_alpha, window_size=CFG.moving_average_window)
    gestures = GestureController(
        pinch_threshold=CFG.pinch_threshold,
        hold_seconds=CFG.gesture_hold_seconds,
        click_cooldown_seconds=CFG.click_cooldown_seconds,
        scroll_gain=CFG.scroll_gain,
    )

    prev_time = time.time()

    try:
        while True:
            frame = camera.read()
            if frame is None:
                continue

            hand_landmarks, _ = hand_tracker.process(frame)
            gesture_result = gestures.detect(hand_landmarks)

            tracking = hand_landmarks is not None
            paused = gesture_result["paused"]

            if gesture_result["pen_active"] and not paused:
                pen_x, pen_y = gesture_result["pen_point"]
                target = cursor.map_pen_to_screen(pen_x, pen_y)
                smoothed = smoother.update(target)
                cursor.move_cursor(int(smoothed[0]), int(smoothed[1]))
            else:
                smoother.reset()

            if gesture_result["click"]:
                cursor.left_click()
            if gesture_result["drag_down"]:
                cursor.drag_down()
            if gesture_result["drag_up"]:
                cursor.drag_up()
            if gesture_result["scroll_mode"] and abs(gesture_result["scroll_delta"]) > 0:
                cursor.scroll(gesture_result["scroll_delta"])

            now = time.time()
            fps = 1.0 / max(now - prev_time, 1e-6)
            prev_time = now

            draw_status(
                frame,
                fps=fps,
                tracking=tracking,
                gesture=gesture_result["gesture"],
                dragging=gesture_result["dragging"],
                paused=paused,
            )

            cv2.imshow("Touchless Cursor (Pen + Gestures)", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break

    finally:
        camera.release()
        hand_tracker.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
