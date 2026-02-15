from collections import deque
from typing import Deque, Optional, Tuple


class ExponentialPointFilter:
    def __init__(self, alpha: float = 0.3):
        self.alpha = alpha
        self._value: Optional[Tuple[float, float]] = None

    def reset(self) -> None:
        self._value = None

    def update(self, point: Tuple[float, float]) -> Tuple[float, float]:
        if self._value is None:
            self._value = point
            return point

        x = self.alpha * point[0] + (1.0 - self.alpha) * self._value[0]
        y = self.alpha * point[1] + (1.0 - self.alpha) * self._value[1]
        self._value = (x, y)
        return self._value


class MovingAveragePointFilter:
    def __init__(self, window_size: int = 4):
        self.window_size = window_size
        self._buffer: Deque[Tuple[float, float]] = deque(maxlen=window_size)

    def reset(self) -> None:
        self._buffer.clear()

    def update(self, point: Tuple[float, float]) -> Tuple[float, float]:
        self._buffer.append(point)
        count = len(self._buffer)
        sx = sum(p[0] for p in self._buffer)
        sy = sum(p[1] for p in self._buffer)
        return (sx / count, sy / count)
