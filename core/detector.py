from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np
import cv2
from ultralytics import YOLO
from ultralytics import settings
from config import config

settings.update({"weights_dir": "models"})

@dataclass
class DetectionResult:
    label: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x1, y1, x2, y2 pixels
    distance_m: Optional[float] = None
    track_id: Optional[int] = None

class Detector:
    def __init__(self):
        self.model = YOLO(config.YOLO_MODEL)
        
    def detect(self, frame: np.ndarray) -> List[DetectionResult]:
        # run inference, filter by config.CONFIDENCE_MIN, max config.MAX_DETECTIONS results
        results = self.model(frame, verbose=False)[0]
        
        detections = []
        for box in results.boxes:
            conf = float(box.conf[0])
            if conf >= config.CONFIDENCE_MIN:
                label_idx = int(box.cls[0])
                label = self.model.names[label_idx]
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                detections.append(DetectionResult(
                    label=label,
                    confidence=conf,
                    bbox=(x1, y1, x2, y2)
                ))
                
        # sort by descending confidence, return up to max detections
        detections.sort(key=lambda x: x.confidence, reverse=True)
        return detections[:config.MAX_DETECTIONS]

    def draw(self, frame: np.ndarray, results: List[DetectionResult]) -> np.ndarray:
        annotated = frame.copy()
        for det in results:
            x1, y1, x2, y2 = det.bbox
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # label text with distance if available
            label_text = f"{det.label} {det.confidence:.2f}"
            if det.distance_m is not None:
                label_text += f" | {det.distance_m:.1f}m"
            if det.track_id is not None:
                label_text = f"[{det.track_id}] " + label_text
                
            cv2.putText(annotated, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
        return annotated
