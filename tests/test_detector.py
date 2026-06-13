import numpy as np
from core.detector import Detector
from config import config

def test_detector():
    d = Detector()
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    results = d.detect(frame)
    assert isinstance(results, list)
    for det in results:
        assert det.confidence >= config.CONFIDENCE_MIN
