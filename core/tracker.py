from typing import List, Dict
from core.detector import DetectionResult
from config import config

def calculate_iou(box1: tuple, box2: tuple) -> float:
    # box = (x1, y1, x2, y2)
    x1_inter = max(box1[0], box2[0])
    y1_inter = max(box1[1], box2[1])
    x2_inter = min(box1[2], box2[2])
    y2_inter = min(box1[3], box2[3])

    if x2_inter < x1_inter or y2_inter < y1_inter:
        return 0.0
        
    inter_area = (x2_inter - x1_inter) * (y2_inter - y1_inter)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    
    iou = inter_area / float(box1_area + box2_area - inter_area)
    return iou

class Tracker:
    def __init__(self):
        self.next_track_id = 0
        # mapping track_id -> (DetectionResult, frames_missed)
        self.tracks: Dict[int, tuple[DetectionResult, int]] = {}
        
    def update(self, detections: List[DetectionResult]) -> List[DetectionResult]:
        matched_detections = []
        
        # Sort incoming detections by confidence
        unmatched_detections = sorted(detections, key=lambda x: x.confidence, reverse=True)
        unmatched_tracks = set(self.tracks.keys())
        
        # Greedy matching by max IoU
        for det in unmatched_detections[:]:
            best_iou = -1.0
            best_track_id = None
            
            for track_id in unmatched_tracks:
                track_det, _ = self.tracks[track_id]
                if track_det.label == det.label: # Only match same classes
                    iou = calculate_iou(det.bbox, track_det.bbox)
                    if iou > best_iou:
                        best_iou = iou
                        best_track_id = track_id
                        
            if best_iou >= config.IOU_THRESHOLD and best_track_id is not None:
                det.track_id = best_track_id
                matched_detections.append(det)
                unmatched_detections.remove(det)
                unmatched_tracks.remove(best_track_id)
                self.tracks[best_track_id] = (det, 0)
                
        # Assign new IDs to unmatched detections
        for det in unmatched_detections:
            det.track_id = self.next_track_id
            self.next_track_id += 1
            matched_detections.append(det)
            self.tracks[det.track_id] = (det, 0)
            
        # Update missing tracks
        for track_id in list(unmatched_tracks):
            det, missed = self.tracks[track_id]
            missed += 1
            if missed > config.TRACKER_MAX_MISS_FRAMES:
                del self.tracks[track_id]
            else:
                self.tracks[track_id] = (det, missed)
                
        # Return detections with track_ids, original order doesn't matter much
        return matched_detections
