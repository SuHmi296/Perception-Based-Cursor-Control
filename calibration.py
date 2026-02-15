import json
from pathlib import Path
from typing import List, Optional, Tuple

from utils.math_utils import clamp


CALIBRATION_POINTS = [
    (0.1, 0.1),
    (0.9, 0.1),
    (0.5, 0.5),
    (0.1, 0.9),
    (0.9, 0.9),
]


class CalibrationProfile:
    def __init__(self, scale_x: float = 1.0, scale_y: float = 1.0, offset_x: float = 0.0, offset_y: float = 0.0):
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.offset_x = offset_x
        self.offset_y = offset_y

    def apply(self, gaze: Tuple[float, float]) -> Tuple[float, float]:
        x = clamp(gaze[0] * self.scale_x + self.offset_x, 0.0, 1.0)
        y = clamp(gaze[1] * self.scale_y + self.offset_y, 0.0, 1.0)
        return x, y

    def save(self, path: str = "calibration.json") -> None:
        payload = {
            "scale_x": self.scale_x,
            "scale_y": self.scale_y,
            "offset_x": self.offset_x,
            "offset_y": self.offset_y,
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @staticmethod
    def load(path: str = "calibration.json"):
        p = Path(path)
        if not p.exists():
            return CalibrationProfile()
        payload = json.loads(p.read_text(encoding="utf-8"))
        return CalibrationProfile(
            scale_x=float(payload.get("scale_x", 1.0)),
            scale_y=float(payload.get("scale_y", 1.0)),
            offset_x=float(payload.get("offset_x", 0.0)),
            offset_y=float(payload.get("offset_y", 0.0)),
        )


class CalibrationSession:
    def __init__(self):
        self.active = False
        self.current_index = 0
        self.samples: List[List[Tuple[float, float]]] = [[] for _ in CALIBRATION_POINTS]

    def start(self) -> None:
        self.active = True
        self.current_index = 0
        self.samples = [[] for _ in CALIBRATION_POINTS]

    def add_sample(self, gaze: Optional[Tuple[float, float]]) -> None:
        if not self.active or gaze is None:
            return
        self.samples[self.current_index].append(gaze)

    def capture_current_point(self) -> bool:
        if not self.active:
            return False
        if len(self.samples[self.current_index]) < 8:
            return False
        self.current_index += 1
        if self.current_index >= len(CALIBRATION_POINTS):
            self.active = False
            return True
        return False

    def current_target(self) -> Optional[Tuple[float, float]]:
        if not self.active:
            return None
        return CALIBRATION_POINTS[self.current_index]

    def build_profile(self) -> CalibrationProfile:
        observed = []
        for point_samples in self.samples:
            if point_samples:
                x = sum(p[0] for p in point_samples) / len(point_samples)
                y = sum(p[1] for p in point_samples) / len(point_samples)
                observed.append((x, y))
        if len(observed) < 3:
            return CalibrationProfile()

        exp_x = [p[0] for p in CALIBRATION_POINTS]
        exp_y = [p[1] for p in CALIBRATION_POINTS]
        obs_x = [p[0] for p in observed]
        obs_y = [p[1] for p in observed]

        obs_min_x, obs_max_x = min(obs_x), max(obs_x)
        obs_min_y, obs_max_y = min(obs_y), max(obs_y)
        exp_min_x, exp_max_x = min(exp_x), max(exp_x)
        exp_min_y, exp_max_y = min(exp_y), max(exp_y)

        if abs(obs_max_x - obs_min_x) < 1e-4 or abs(obs_max_y - obs_min_y) < 1e-4:
            return CalibrationProfile()

        scale_x = (exp_max_x - exp_min_x) / (obs_max_x - obs_min_x)
        scale_y = (exp_max_y - exp_min_y) / (obs_max_y - obs_min_y)
        offset_x = exp_min_x - obs_min_x * scale_x
        offset_y = exp_min_y - obs_min_y * scale_y

        return CalibrationProfile(scale_x=scale_x, scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)
