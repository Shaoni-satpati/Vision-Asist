from unittest.mock import patch
import numpy as np
from core.pipeline import Pipeline
from core.detector import DetectionResult
from config import config

@patch("core.narrator.Narrator._run")
@patch("core.camera.Camera.get_frame")
@patch("core.detector.Detector.detect")
@patch("core.detector.Detector.draw")
def test_pipeline(mock_draw, mock_detect, mock_get_frame, mock_narrator_run):
    mock_get_frame.return_value = np.zeros((480, 640, 3), dtype=np.uint8)
    mock_detect.return_value = [DetectionResult(label="person", confidence=0.8, bbox=(10, 10, 100, 100))]
    mock_draw.return_value = np.zeros((480, 640, 3), dtype=np.uint8)
    
    pipeline = Pipeline()
    frame_bytes = pipeline.process_frame()
    
    assert frame_bytes is not None
    assert frame_bytes.startswith(b"\xff\xd8")
    
    pipeline.shutdown()
