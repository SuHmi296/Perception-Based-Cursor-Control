import cv2

try:
    import mediapipe as mp
except Exception as exc:
    raise RuntimeError("MediaPipe is not installed correctly.") from exc


def _get_face_mesh_module():
    if hasattr(mp, "solutions") and hasattr(mp.solutions, "face_mesh"):
        return mp.solutions.face_mesh
    raise RuntimeError(
        "This project requires MediaPipe Solutions API (mp.solutions.face_mesh). "
        "Install a compatible version: pip install mediapipe==0.10.14"
    )


class FaceTracker:
    def __init__(self, min_detection_confidence: float, min_tracking_confidence: float):
        self._mp_face_mesh = _get_face_mesh_module()
        self._face_mesh = self._mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def process(self, frame_bgr):
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        result = self._face_mesh.process(rgb)
        if not result.multi_face_landmarks:
            return None
        return result.multi_face_landmarks[0]

    def close(self) -> None:
        self._face_mesh.close()
