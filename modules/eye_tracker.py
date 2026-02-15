from typing import Optional, Tuple

from utils.math_utils import clamp, normalized_ratio


LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]
LEFT_EYE_OUTER = 33
LEFT_EYE_INNER = 133
RIGHT_EYE_INNER = 362
RIGHT_EYE_OUTER = 263
LEFT_EYE_UPPER = 159
LEFT_EYE_LOWER = 145
RIGHT_EYE_UPPER = 386
RIGHT_EYE_LOWER = 374


class EyeTracker:
    def __init__(self, alpha: float = 0.22):
        self.alpha = alpha
        self._filtered: Optional[Tuple[float, float]] = None

    @staticmethod
    def _landmark_xy(landmarks, idx: int, frame_width: int, frame_height: int) -> Tuple[float, float]:
        lm = landmarks.landmark[idx]
        return lm.x * frame_width, lm.y * frame_height

    def _iris_center(self, landmarks, iris_indices, frame_width: int, frame_height: int) -> Tuple[float, float]:
        points = [self._landmark_xy(landmarks, idx, frame_width, frame_height) for idx in iris_indices]
        cx = sum(p[0] for p in points) / len(points)
        cy = sum(p[1] for p in points) / len(points)
        return cx, cy

    def reset(self) -> None:
        self._filtered = None

    def _smooth(self, gaze: Tuple[float, float]) -> Tuple[float, float]:
        if self._filtered is None:
            self._filtered = gaze
            return gaze
        x = self.alpha * gaze[0] + (1.0 - self.alpha) * self._filtered[0]
        y = self.alpha * gaze[1] + (1.0 - self.alpha) * self._filtered[1]
        self._filtered = (x, y)
        return self._filtered

    def estimate_gaze(self, landmarks, frame_width: int, frame_height: int) -> Optional[Tuple[float, float]]:
        if landmarks is None:
            self.reset()
            return None

        li = self._iris_center(landmarks, LEFT_IRIS, frame_width, frame_height)
        ri = self._iris_center(landmarks, RIGHT_IRIS, frame_width, frame_height)

        left_outer_x, _ = self._landmark_xy(landmarks, LEFT_EYE_OUTER, frame_width, frame_height)
        left_inner_x, _ = self._landmark_xy(landmarks, LEFT_EYE_INNER, frame_width, frame_height)
        right_inner_x, _ = self._landmark_xy(landmarks, RIGHT_EYE_INNER, frame_width, frame_height)
        right_outer_x, _ = self._landmark_xy(landmarks, RIGHT_EYE_OUTER, frame_width, frame_height)

        left_upper_y = self._landmark_xy(landmarks, LEFT_EYE_UPPER, frame_width, frame_height)[1]
        left_lower_y = self._landmark_xy(landmarks, LEFT_EYE_LOWER, frame_width, frame_height)[1]
        right_upper_y = self._landmark_xy(landmarks, RIGHT_EYE_UPPER, frame_width, frame_height)[1]
        right_lower_y = self._landmark_xy(landmarks, RIGHT_EYE_LOWER, frame_width, frame_height)[1]

        left_x0, left_x1 = sorted((left_outer_x, left_inner_x))
        right_x0, right_x1 = sorted((right_outer_x, right_inner_x))
        left_y0, left_y1 = sorted((left_upper_y, left_lower_y))
        right_y0, right_y1 = sorted((right_upper_y, right_lower_y))

        gx_left = normalized_ratio(li[0], left_x0, left_x1)
        gx_right = normalized_ratio(ri[0], right_x0, right_x1)
        gy_left = normalized_ratio(li[1], left_y0, left_y1)
        gy_right = normalized_ratio(ri[1], right_y0, right_y1)

        gaze_x = clamp((gx_left + gx_right) * 0.5, 0.0, 1.0)
        gaze_y = clamp((gy_left + gy_right) * 0.5, 0.0, 1.0)
        return self._smooth((gaze_x, gaze_y))
