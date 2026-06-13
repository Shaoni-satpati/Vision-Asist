import numpy as np
from core.depth_estimator import DepthEstimator

def test_depth_estimator():
    de = DepthEstimator()
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    depth_map = de.get_depth_map(frame)
    
    if depth_map is not None:
        assert depth_map.shape == (480, 640)
        assert depth_map.dtype == np.float32
        
        distance = de.estimate_distance(depth_map, (100, 100, 200, 200))
        assert 0.3 <= distance <= 20.0
