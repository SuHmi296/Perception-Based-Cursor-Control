# Touchless Cursor (Eye + Hand Gesture)

## Controls
- Index fingertip acts as a virtual pen for cursor movement.
- `pinch` -> left click
- `fist` -> drag hold
- `two_fingers` -> scroll mode
- `open_palm` -> pause pen tracking (lets you use touchpad normally)
- `ESC` -> emergency stop

## Notes
- Cursor mapping is tuned from `config.py` (`invert_x`, margins, sensitivity, smoothing).

## Setup (Windows PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Run
```powershell
python main.py
```

## Note
This project depends on MediaPipe `solutions` API, so `mediapipe==0.10.14` is pinned.
