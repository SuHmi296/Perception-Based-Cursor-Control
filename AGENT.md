Agent.md
Project: Touchless Cursor (Eye + Gesture Controlled System)
1. Project Overview

Touchless Cursor is an AI-powered human-computer interaction system that allows users to:

Move cursor using eye gaze

Perform clicks using hand gestures

Scroll and drag using finger combinations

Operate computer without physical mouse

The system uses:

Webcam input

Face landmark detection

Hand landmark detection

OS-level mouse control

Goal:
Build a clean, smooth, real-time, production-like prototype.

2. Agent Role Definition

This AI coding agent must:

Write modular, maintainable Python code

Prioritize real-time performance

Avoid unnecessary heavy models

Use landmark-based logic instead of deep training

Always implement smoothing and safety logic

Structure code in scalable architecture

Avoid monolithic scripts

3. High-Level Architecture
touchless-cursor/
│
├── main.py
├── config.py
├── calibration.py
│
├── modules/
│   ├── camera.py
│   ├── face_tracker.py
│   ├── eye_tracker.py
│   ├── hand_tracker.py
│   ├── gesture_controller.py
│   ├── cursor_controller.py
│   ├── smoothing.py
│
├── utils/
│   ├── math_utils.py
│   ├── filters.py
│
└── Agent.md

4. Development Phases (Agent Execution Plan)
Phase 1 — Base Setup

Agent Tasks:

Initialize webcam stream

Integrate face landmark detection

Integrate hand landmark detection

Display debug overlay (landmarks + FPS)

Success Criteria:

Stable 25+ FPS

No blocking calls

Clean window rendering

Phase 2 — Eye-Based Cursor Movement

Agent Tasks:

Extract iris center coordinates

Normalize gaze relative to frame

Map camera coordinates → screen resolution

Add smoothing filter

Move cursor using OS-level control

Required Features:

Dead zone in center

Adjustable sensitivity

Jitter reduction

Cursor Mapping Formula:

screen_x = (gaze_x / frame_width) * screen_width
screen_y = (gaze_y / frame_height) * screen_height


Then apply smoothing:

smoothed_x = alpha * new_x + (1 - alpha) * previous_x

Phase 3 — Gesture Detection

Agent Tasks:

Detect gestures using finger landmark distances.

Gesture Definitions:

Pinch (thumb + index close) → Left click

Two fingers up → Scroll mode

Fist → Drag

Open palm → Reset

Gesture Logic Example:

if distance(thumb_tip, index_tip) < threshold:
    trigger_click()


Must include:

Cooldown timer

Hold duration requirement

False positive prevention

Phase 4 — Safety & Stability

Agent must implement:

Gesture cooldown system

Click debouncing

Eye tracking fallback (if face lost)

Frame drop tolerance

Emergency stop key (ESC)

Phase 5 — Calibration System

Add:

5-point calibration grid

Store mapping offset

Sensitivity slider

Smoothing slider

Calibration improves demo quality significantly.

5. Technical Requirements

The agent must ensure:

Modular architecture

No global spaghetti state

Clean separation:

Vision layer

Control logic

OS interaction

Maintain >20 FPS

Use non-blocking loops

6. Core Algorithms
Eye Direction Estimation

Compute relative iris position between:

Left eye corner

Right eye corner

Normalize:

relative_x = (iris_x - left_corner_x) / eye_width


This makes it resolution-independent.

Gesture Stability Check

Require gesture to persist:

if gesture_detected_for >= 0.5 seconds:
    execute_action()


Prevents accidental triggers.

Cursor Smoothing Filter

Use moving average buffer:

buffer.append(new_position)
if len(buffer) > N:
    buffer.pop(0)

smoothed_position = average(buffer)

7. Performance Guidelines

Agent must:

Avoid heavy neural models

Avoid retraining

Use landmark geometry only

Minimize per-frame allocations

Predefine reusable buffers

8. UI/UX Enhancements (Advanced Look)

Add:

Cursor trail effect

On-screen gesture indicator

Mode toggle display

Real-time FPS counter

Status badge (Tracking / Lost / Clicking)

Clean UI makes project look 10x more advanced.

9. Stretch Goals (Optional Advanced)

If time allows:

Eye blink click option

Voice toggle mode

Multi-monitor support

Adaptive smoothing based on speed

User profile save system

10. Constraints

Agent must NOT:

Overcomplicate with deep learning training

Hardcode screen resolution

Use blocking sleep calls

Trigger multiple clicks per frame

Combine everything inside main.py

11. Final Demo Flow

Launch system

Calibrate

Move cursor with eyes

Click with pinch

Drag with fist

Scroll with two fingers

Show smooth tracking

Goal:
Looks futuristic, stable, intentional.

12. Project Positioning Statement

Touchless Cursor:
An AI-powered accessibility and futuristic interaction system that enables fully hands-free computing through real-time eye tracking and gesture recognition.