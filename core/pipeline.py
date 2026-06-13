import cv2
from core.camera import Camera
from core.detector import Detector
from core.depth_estimator import DepthEstimator
from core.narrator import Narrator
from core.tracker import Tracker
from config import config

class Pipeline:
    def __init__(self):
        self.camera   = Camera()
        self.detector = Detector()
        self.depth    = DepthEstimator()
        self.narrator = Narrator()
        self.tracker  = Tracker()
        
        self.frame_count = 0
        self.last_depth_map = None

    def process_frame(self) -> bytes | None:
        """
        Grab one frame, run the full pipeline, return JPEG bytes for streaming.
        Returns None if no frame is available.
        """
        frame = self.camera.get_frame()
        if frame is None:
            return None

        # Performance: skip depth every N frames
        self.frame_count += 1
        
        # Performance notes: Run YOLO on a downscaled frame
        frame_small = cv2.resize(frame, (320, 240))
        detections = self.detector.detect(frame_small)
        
        # Scale bounding boxes back up
        scale_x = frame.shape[1] / 320.0
        scale_y = frame.shape[0] / 240.0
        for det in detections:
            x1, y1, x2, y2 = det.bbox
            det.bbox = (int(x1 * scale_x), int(y1 * scale_y), int(x2 * scale_x), int(y2 * scale_y))

        if config.DEPTH_ENABLED:
            # Depth runs every 3rd frame
            if self.frame_count % 3 == 1 or self.last_depth_map is None:
                self.last_depth_map = self.depth.get_depth_map(frame)
                
            for det in detections:
                det.distance_m = self.depth.estimate_distance(self.last_depth_map, det.bbox)

        detections = self.tracker.update(detections)

        for det in detections:
            # use track_id as the cooldown key instead of label
            key_label = f"[{det.track_id}] {det.label}" if det.track_id is not None else det.label
            self.narrator.narrate(key_label, det.distance_m)

        annotated = self.detector.draw(frame, detections)

        _, jpeg = cv2.imencode(".jpg", annotated, [cv2.IMWRITE_JPEG_QUALITY, 75])
        return jpeg.tobytes()

    def shutdown(self):
        self.camera.release()
        self.narrator.shutdown()
