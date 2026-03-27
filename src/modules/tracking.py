"""
Module 3: Real-Time Multi-Target Tracking
ByteTrack implementation for persistent target tracking with occlusion handling.
"""
import numpy as np
from typing import List, Optional, Tuple
from datetime import datetime
from collections import deque
import logging

from scipy.optimize import linear_sum_assignment
from filterpy.kalman import KalmanFilter

from ..core.models import Detection, TrackObject, BoundingBox, TrajectoryPoint, Velocity, FrameData
from ..core.utils import iou, calculate_velocity

logger = logging.getLogger(__name__)


class KalmanBoxTracker:
    """Kalman filter for tracking bounding boxes."""
    
    count = 0
    
    def __init__(self, bbox: BoundingBox, class_name: str, confidence: float):
        """
        Initialize Kalman tracker.
        
        Args:
            bbox: Initial bounding box
            class_name: Object class
            confidence: Detection confidence
        """
        # State: [x, y, w, h, vx, vy, vw, vh]
        self.kf = KalmanFilter(dim_x=8, dim_z=4)
        
        # State transition matrix
        self.kf.F = np.array([
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1]
        ])
        
        # Measurement matrix
        self.kf.H = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0]
        ])
        
        # Measurement noise - reduced for smoother tracking
        self.kf.R *= 5.0
        
        # Process noise - optimized for persistent tracking
        self.kf.P[4:, 4:] *= 500.0  # Velocity uncertainty
        self.kf.P *= 5.0  # Position uncertainty
        
        # Process noise covariance - smoother predictions
        self.kf.Q[-1, -1] *= 0.005  # Very low noise for size changes
        self.kf.Q[4:, 4:] *= 0.005  # Low noise for velocity changes
        
        # Initialize state
        self.kf.x[:4] = np.array([bbox.x, bbox.y, bbox.w, bbox.h]).reshape(4, 1)
        
        self.time_since_update = 0
        self.id = KalmanBoxTracker.count
        KalmanBoxTracker.count += 1
        self.history = []
        self.hits = 0
        self.hit_streak = 0
        self.age = 0
        self.class_name = class_name
        self.confidence = confidence
    
    def update(self, bbox: BoundingBox, confidence: float):
        """
        Update tracker with new detection.
        
        Args:
            bbox: New bounding box
            confidence: Detection confidence
        """
        self.time_since_update = 0
        self.history = []
        self.hits += 1
        self.hit_streak += 1
        self.confidence = confidence
        
        # Update Kalman filter
        measurement = np.array([bbox.x, bbox.y, bbox.w, bbox.h]).reshape(4, 1)
        self.kf.update(measurement)
    
    def predict(self) -> BoundingBox:
        """
        Predict next state.
        
        Returns:
            Predicted bounding box
        """
        # Prevent negative width/height
        if self.kf.x[2] + self.kf.x[6] <= 0:
            self.kf.x[6] = 0
        if self.kf.x[3] + self.kf.x[7] <= 0:
            self.kf.x[7] = 0
        
        self.kf.predict()
        self.age += 1
        
        if self.time_since_update > 0:
            self.hit_streak = 0
        self.time_since_update += 1
        
        self.history.append(self.get_state())
        return self.get_state()
    
    def get_state(self) -> BoundingBox:
        """
        Get current state as bounding box.
        
        Returns:
            Current bounding box
        """
        state = self.kf.x[:4].flatten()
        return BoundingBox(
            x=float(state[0]),
            y=float(state[1]),
            w=float(state[2]),
            h=float(state[3])
        )
    
    def get_velocity(self) -> Tuple[float, float]:
        """
        Get velocity from Kalman state.
        
        Returns:
            (vx, vy) velocity tuple
        """
        return float(self.kf.x[4][0]), float(self.kf.x[5][0])


class ByteTracker:
    """ByteTrack multi-object tracker."""
    
    def __init__(
        self,
        track_thresh: float = 0.5,
        track_buffer: int = 90,
        match_thresh: float = 0.8,
        min_box_area: int = 100,
        trajectory_history: int = 30
    ):
        """
        Initialize ByteTrack tracker.
        
        Args:
            track_thresh: High confidence threshold
            track_buffer: Number of frames to keep lost tracks
            match_thresh: IoU threshold for matching
            min_box_area: Minimum box area to consider
            trajectory_history: Number of trajectory points to keep
        """
        self.track_thresh = track_thresh
        self.track_buffer = track_buffer
        self.match_thresh = match_thresh
        self.min_box_area = min_box_area
        self.trajectory_history = trajectory_history
        
        self.tracked_tracks: List[KalmanBoxTracker] = []
        self.lost_tracks: List[KalmanBoxTracker] = []
        self.removed_tracks: List[KalmanBoxTracker] = []
        
        self.frame_id = 0
        self.trajectories: dict = {}  # track_id -> deque of (x, y, timestamp)
        
        # Metrics
        self.total_tracks = 0
        self.id_switches = 0
    
    def update(
        self,
        detections: List[Detection],
        frame_data: FrameData
    ) -> List[TrackObject]:
        """
        Update tracker with new detections.
        
        Args:
            detections: List of detections
            frame_data: Frame metadata
        
        Returns:
            List of active tracks
        """
        self.frame_id += 1
        
        # Separate high and low confidence detections
        high_conf_dets = []
        low_conf_dets = []
        
        for det in detections:
            if det.bbox.area >= self.min_box_area:
                if det.confidence >= self.track_thresh:
                    high_conf_dets.append(det)
                else:
                    low_conf_dets.append(det)
        
        # Predict all tracks
        for track in self.tracked_tracks:
            track.predict()
        
        # First association: high confidence detections with tracked tracks
        unmatched_tracks, unmatched_dets = self._associate(
            self.tracked_tracks, high_conf_dets, self.match_thresh
        )
        
        # Second association: low confidence detections with unmatched tracks
        unmatched_tracks_2, unmatched_low_dets = self._associate(
            [self.tracked_tracks[i] for i in unmatched_tracks],
            low_conf_dets,
            0.5  # Lower threshold for low confidence
        )
        
        # Update matched tracks
        for track_idx, det_idx in self._get_matched_pairs(
            self.tracked_tracks, high_conf_dets, unmatched_tracks, unmatched_dets
        ):
            track = self.tracked_tracks[track_idx]
            det = high_conf_dets[det_idx]
            track.update(det.bbox, det.confidence)
            
            # Update trajectory
            center = det.bbox.center
            if track.id not in self.trajectories:
                self.trajectories[track.id] = deque(maxlen=self.trajectory_history)
            self.trajectories[track.id].append((center[0], center[1], frame_data.timestamp))
        
        # Handle unmatched tracks
        for i in unmatched_tracks_2:
            track = self.tracked_tracks[i]
            if track.time_since_update <= self.track_buffer:
                # Keep in tracked but mark as lost
                pass
            else:
                # Move to lost tracks
                self.lost_tracks.append(track)
        
        # Remove old lost tracks
        self.tracked_tracks = [
            t for t in self.tracked_tracks
            if t.time_since_update <= self.track_buffer
        ]
        
        # Initialize new tracks from unmatched high confidence detections
        for i in unmatched_dets:
            det = high_conf_dets[i]
            new_track = KalmanBoxTracker(det.bbox, det.class_name.value, det.confidence)
            self.tracked_tracks.append(new_track)
            self.total_tracks += 1
            
            # Initialize trajectory
            center = det.bbox.center
            self.trajectories[new_track.id] = deque(maxlen=self.trajectory_history)
            self.trajectories[new_track.id].append((center[0], center[1], frame_data.timestamp))
        
        # Build output tracks - include recently seen tracks for persistence
        output_tracks = []
        for track in self.tracked_tracks:
            # Output tracks that are active or recently lost (within 30 frames = 1 second)
            if track.hit_streak >= 1 and track.time_since_update <= 30:
                bbox = track.get_state()
                
                # Get trajectory
                trajectory = []
                if track.id in self.trajectories:
                    for x, y, ts in self.trajectories[track.id]:
                        trajectory.append(TrajectoryPoint(x=x, y=y, timestamp=ts))
                
                # Calculate velocity
                velocity = None
                if len(trajectory) >= 2:
                    vx, vy = track.get_velocity()
                    velocity = Velocity(vx=vx, vy=vy)
                
                # Create track object
                track_obj = TrackObject(
                    track_id=track.id,
                    class_name=track.class_name,
                    confidence=track.confidence,
                    bbox=bbox,
                    velocity=velocity,
                    trajectory=trajectory,
                    last_seen=frame_data.timestamp,
                    frames_since_update=track.time_since_update
                )
                
                output_tracks.append(track_obj)
        
        return output_tracks
    
    def _associate(
        self,
        tracks: List[KalmanBoxTracker],
        detections: List[Detection],
        iou_threshold: float
    ) -> Tuple[List[int], List[int]]:
        """
        Associate tracks with detections using IoU.
        
        Returns:
            (unmatched_track_indices, unmatched_detection_indices)
        """
        if len(tracks) == 0 or len(detections) == 0:
            return list(range(len(tracks))), list(range(len(detections)))
        
        # Compute IoU matrix
        iou_matrix = np.zeros((len(tracks), len(detections)))
        for t, track in enumerate(tracks):
            track_box = track.get_state().to_xyxy()
            for d, det in enumerate(detections):
                det_box = det.bbox.to_xyxy()
                iou_matrix[t, d] = iou(track_box, det_box)
        
        # Hungarian algorithm
        if iou_matrix.max() > iou_threshold:
            matched_indices = linear_sum_assignment(-iou_matrix)
            matched_indices = np.array(list(zip(*matched_indices)))
            
            unmatched_tracks = []
            for t in range(len(tracks)):
                if t not in matched_indices[:, 0]:
                    unmatched_tracks.append(t)
            
            unmatched_dets = []
            for d in range(len(detections)):
                if d not in matched_indices[:, 1]:
                    unmatched_dets.append(d)
            
            # Filter matches by threshold
            matches = []
            for m in matched_indices:
                if iou_matrix[m[0], m[1]] < iou_threshold:
                    unmatched_tracks.append(m[0])
                    unmatched_dets.append(m[1])
                else:
                    matches.append(m)
            
            return unmatched_tracks, unmatched_dets
        else:
            return list(range(len(tracks))), list(range(len(detections)))
    
    def _get_matched_pairs(
        self,
        tracks: List[KalmanBoxTracker],
        detections: List[Detection],
        unmatched_tracks: List[int],
        unmatched_dets: List[int]
    ) -> List[Tuple[int, int]]:
        """Get matched (track_idx, det_idx) pairs."""
        all_tracks = set(range(len(tracks)))
        all_dets = set(range(len(detections)))
        
        matched_tracks = all_tracks - set(unmatched_tracks)
        matched_dets = all_dets - set(unmatched_dets)
        
        # Reconstruct pairs
        pairs = []
        for t_idx in matched_tracks:
            for d_idx in matched_dets:
                pairs.append((t_idx, d_idx))
        
        return pairs
    
    def get_track_by_id(self, track_id: int) -> Optional[KalmanBoxTracker]:
        """Get track by ID."""
        for track in self.tracked_tracks:
            if track.id == track_id:
                return track
        return None
