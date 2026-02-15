from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    camera_index: int = 0
    frame_width: int = 1280
    frame_height: int = 720

    hand_min_detection_confidence: float = 0.6
    hand_min_tracking_confidence: float = 0.5

    cursor_sensitivity_x: float = 1.05
    cursor_sensitivity_y: float = 1.0
    invert_x: bool = False
    invert_y: bool = False
    max_cursor_step_px: int = 45
    pen_active_margin_x: float = 0.15
    pen_active_margin_y: float = 0.18

    smoothing_alpha: float = 0.18
    moving_average_window: int = 6

    pinch_threshold: float = 0.055
    gesture_hold_seconds: float = 0.22
    click_cooldown_seconds: float = 0.45

    scroll_gain: float = 65.0


CFG = Config()
