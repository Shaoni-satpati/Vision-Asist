import torch
import numpy as np
import cv2
from config import config

class DepthEstimator:
    def __init__(self):
        if not config.DEPTH_ENABLED:
            return
            
        self.device = (
            "cuda" if torch.cuda.is_available() else
            "mps" if torch.backends.mps.is_available() else
            "cpu"
        )
        self.model = torch.hub.load("intel-isl/MiDaS", config.DEPTH_MODEL)
        self.model.to(self.device)
        self.model.eval()
        
        transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
        if config.DEPTH_MODEL == "MiDaS_small":
            self.transform = transforms.small_transform
        else:
            self.transform = transforms.dpt_transform

    def get_depth_map(self, frame: np.ndarray) -> np.ndarray | None:
        if not config.DEPTH_ENABLED:
            return None
            
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        input_batch = self.transform(img).to(self.device)

        with torch.no_grad():
            prediction = self.model(input_batch)
            
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()

        output = prediction.cpu().numpy()
        return output

    def estimate_distance(self, depth_map: np.ndarray, bbox: tuple) -> float:
        x1, y1, x2, y2 = bbox
        
        # Crop the depth map to the bounding box region
        cropped_depth = depth_map[y1:y2, x1:x2]
        
        # Take the median of the cropped values
        median_depth = np.median(cropped_depth)
        
        # Convert relative inverse depth to an approximate distance in metres
        # using heuristic
        distance_m = config.DEPTH_SCALE / (median_depth + 1e-6)
        
        # Clamp to [0.3, 20.0] metres
        return min(max(distance_m, 0.3), 20.0)
