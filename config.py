import os
from dataclasses import dataclass

@dataclass
class Config:
    CAMERA_INDEX: int = int(os.getenv("CAMERA_INDEX", "0"))
    FRAME_WIDTH: int = int(os.getenv("FRAME_WIDTH", "640"))
    FRAME_HEIGHT: int = int(os.getenv("FRAME_HEIGHT", "480"))
    FPS_TARGET: int = int(os.getenv("FPS_TARGET", "15"))

    YOLO_MODEL: str = os.getenv("YOLO_MODEL", "yolov8n.pt")
    CONFIDENCE_MIN: float = float(os.getenv("CONFIDENCE_MIN", "0.45"))
    IOU_THRESHOLD: float = float(os.getenv("IOU_THRESHOLD", "0.5"))
    MAX_DETECTIONS: int = int(os.getenv("MAX_DETECTIONS", "10"))
    TRACKER_MAX_MISS_FRAMES: int = int(os.getenv("TRACKER_MAX_MISS_FRAMES", "5"))

    DEPTH_MODEL: str = os.getenv("DEPTH_MODEL", "MiDaS_small")
    DEPTH_ENABLED: bool = os.getenv("DEPTH_ENABLED", "True").lower() in ("true", "1", "t")
    DEPTH_SCALE: float = float(os.getenv("DEPTH_SCALE", "10.0"))

    TTS_RATE: int = int(os.getenv("TTS_RATE", "175"))
    TTS_VOLUME: float = float(os.getenv("TTS_VOLUME", "1.0"))
    TTS_COOLDOWN_SEC: float = float(os.getenv("TTS_COOLDOWN_SEC", "2.5"))

    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "5000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

config = Config()
