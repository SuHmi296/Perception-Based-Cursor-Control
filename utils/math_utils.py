import math
from typing import Tuple


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


def distance_2d(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def normalized_ratio(value: float, start: float, end: float) -> float:
    denom = end - start
    if abs(denom) < 1e-6:
        return 0.5
    return (value - start) / denom
