from utils.filters import ExponentialPointFilter, MovingAveragePointFilter


class CursorSmoother:
    def __init__(self, alpha: float, window_size: int):
        self.exp = ExponentialPointFilter(alpha=alpha)
        self.avg = MovingAveragePointFilter(window_size=window_size)

    def reset(self) -> None:
        self.exp.reset()
        self.avg.reset()

    def update(self, point):
        return self.avg.update(self.exp.update(point))
