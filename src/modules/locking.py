"""
Module 4: Target Locking & Prioritization
Manages target locks, priority scoring, and gimbal pointing commands.
"""
import numpy as np
from typing import List, Optional, Dict
from datetime import datetime
import logging

from ..core.models import TrackObject, GimbalCommand, GroundCoordinate, FrameData
from ..core.utils import calculate_gimbal_delta, flat_earth_projection

logger = logging.getLogger(__name__)


class TargetLockManager:
    """Manages target locking and prioritization."""
    
    def __init__(
        self,
        occlusion_tolerance_frames: int = 90,
        priority_weights: Optional[Dict[str, float]] = None,
        class_priority_map: Optional[Dict[str, float]] = None,
        camera_fov_h: float = 60.0,
        camera_fov_v: float = 45.0,
        image_width: int = 640,
        image_height: int = 640
    ):
        """
        Initialize target lock manager.
        
        Args:
            occlusion_tolerance_frames: Frames to maintain lock through occlusion
            priority_weights: Weights for priority scoring
            class_priority_map: Priority values for each class
            camera_fov_h: Camera horizontal FOV in degrees
            camera_fov_v: Camera vertical FOV in degrees
            image_width: Image width in pixels
            image_height: Image height in pixels
        """
        self.occlusion_tolerance = occlusion_tolerance_frames
        self.priority_weights = priority_weights or {
            'distance': 0.4,
            'velocity': 0.3,
            'class_priority': 0.3
        }
        self.class_priority_map = class_priority_map or {
            'person': 1.0,
            'airplane': 0.9,
            'car': 0.8,
            'truck': 0.7,
            'bus': 0.7,
            'motorcycle': 0.6,
            'bicycle': 0.5
        }
        self.camera_fov_h = camera_fov_h
        self.camera_fov_v = camera_fov_v
        self.image_width = image_width
        self.image_height = image_height
        
        self.locked_track_id: Optional[int] = None
        self.lock_timestamp: Optional[datetime] = None
        self.frames_since_lock_seen = 0
        
        # Track history for lock persistence
        self.track_history: Dict[int, List[TrackObject]] = {}
    
    def lock_target(self, track_id: int, tracks: List[TrackObject]) -> bool:
        """
        Lock onto a specific target.
        
        Args:
            track_id: Track ID to lock
            tracks: Current active tracks
        
        Returns:
            True if lock successful, False otherwise
        """
        # Find track
        target_track = None
        for track in tracks:
            if track.track_id == track_id:
                target_track = track
                break
        
        if target_track is None:
            logger.warning(f"Track {track_id} not found, cannot lock")
            return False
        
        self.locked_track_id = track_id
        self.lock_timestamp = datetime.now()
        self.frames_since_lock_seen = 0
        
        logger.info(f"Locked onto track {track_id} ({target_track.class_name})")
        return True
    
    def unlock_target(self):
        """Release current lock."""
        if self.locked_track_id is not None:
            logger.info(f"Unlocked track {self.locked_track_id}")
        
        self.locked_track_id = None
        self.lock_timestamp = None
        self.frames_since_lock_seen = 0
    
    def update_lock(self, tracks: List[TrackObject]) -> Optional[TrackObject]:
        """
        Update lock status and return locked track if active.
        
        Args:
            tracks: Current active tracks
        
        Returns:
            Locked track object or None
        """
        if self.locked_track_id is None:
            return None
        
        # Find locked track
        locked_track = None
        for track in tracks:
            if track.track_id == self.locked_track_id:
                locked_track = track
                track.is_locked = True
                self.frames_since_lock_seen = 0
                break
        
        if locked_track is None:
            # Track not visible
            self.frames_since_lock_seen += 1
            
            if self.frames_since_lock_seen > self.occlusion_tolerance:
                logger.warning(
                    f"Lost lock on track {self.locked_track_id} "
                    f"(exceeded occlusion tolerance: {self.occlusion_tolerance} frames)"
                )
                self.unlock_target()
                return None
            else:
                logger.debug(
                    f"Track {self.locked_track_id} occluded "
                    f"({self.frames_since_lock_seen}/{self.occlusion_tolerance})"
                )
                # Return last known state if available
                if self.locked_track_id in self.track_history:
                    history = self.track_history[self.locked_track_id]
                    if history:
                        return history[-1]
        else:
            # Update track history
            if self.locked_track_id not in self.track_history:
                self.track_history[self.locked_track_id] = []
            self.track_history[self.locked_track_id].append(locked_track)
            
            # Keep only recent history
            if len(self.track_history[self.locked_track_id]) > 30:
                self.track_history[self.locked_track_id] = \
                    self.track_history[self.locked_track_id][-30:]
        
        return locked_track
    
    def compute_gimbal_command(
        self,
        track: TrackObject,
        frame_data: Optional[FrameData] = None
    ) -> GimbalCommand:
        """
        Compute gimbal pointing command to center target.
        
        Args:
            track: Target track
            frame_data: Frame metadata with telemetry
        
        Returns:
            Gimbal command with delta angles
        """
        # Get target center
        center_x, center_y = track.bbox.center
        
        # Calculate gimbal delta
        azimuth_delta, elevation_delta = calculate_gimbal_delta(
            center_x, center_y,
            self.image_width, self.image_height,
            self.camera_fov_h, self.camera_fov_v
        )
        
        return GimbalCommand(
            azimuth=azimuth_delta,
            elevation=elevation_delta
        )
    
    def compute_ground_coordinate(
        self,
        track: TrackObject,
        frame_data: FrameData
    ) -> Optional[GroundCoordinate]:
        """
        Compute ground coordinate of target using flat-earth projection.
        
        Args:
            track: Target track
            frame_data: Frame metadata with telemetry
        
        Returns:
            Ground coordinate or None if telemetry unavailable
        """
        if frame_data.telemetry is None:
            return None
        
        telem = frame_data.telemetry
        center_x, center_y = track.bbox.center
        
        try:
            lat, lon = flat_earth_projection(
                center_x, center_y,
                self.image_width, self.image_height,
                telem.gps.lat, telem.gps.lon,
                telem.altitude,
                telem.gimbal_azimuth,
                telem.gimbal_elevation,
                self.camera_fov_h,
                self.camera_fov_v
            )
            
            return GroundCoordinate(lat=lat, lon=lon, alt=0.0)
        except Exception as e:
            logger.error(f"Failed to compute ground coordinate: {e}")
            return None
    
    def prioritize_tracks(self, tracks: List[TrackObject]) -> List[TrackObject]:
        """
        Score and rank tracks by priority.
        
        Args:
            tracks: List of tracks to prioritize
        
        Returns:
            Sorted list of tracks (highest priority first)
        """
        if not tracks:
            return []
        
        scored_tracks = []
        
        for track in tracks:
            score = self._compute_priority_score(track)
            scored_tracks.append((score, track))
        
        # Sort by score (descending)
        scored_tracks.sort(key=lambda x: x[0], reverse=True)
        
        return [track for _, track in scored_tracks]
    
    def _compute_priority_score(self, track: TrackObject) -> float:
        """
        Compute priority score for a track.
        
        Args:
            track: Track to score
        
        Returns:
            Priority score (higher = more important)
        """
        score = 0.0
        
        # Distance score (closer to center = higher priority)
        center_x, center_y = track.bbox.center
        image_center_x = self.image_width / 2
        image_center_y = self.image_height / 2
        
        distance_from_center = np.sqrt(
            (center_x - image_center_x) ** 2 +
            (center_y - image_center_y) ** 2
        )
        max_distance = np.sqrt(image_center_x ** 2 + image_center_y ** 2)
        distance_score = 1.0 - (distance_from_center / max_distance)
        
        score += self.priority_weights['distance'] * distance_score
        
        # Velocity score (faster = higher priority)
        if track.velocity:
            velocity_magnitude = track.velocity.magnitude
            # Normalize to [0, 1] assuming max velocity of 50 m/s
            velocity_score = min(velocity_magnitude / 50.0, 1.0)
            score += self.priority_weights['velocity'] * velocity_score
        
        # Class priority score
        class_name = track.class_name.value
        class_score = self.class_priority_map.get(class_name, 0.5)
        score += self.priority_weights['class_priority'] * class_score
        
        return score
    
    def get_lock_status(self) -> Dict:
        """
        Get current lock status.
        
        Returns:
            Dict with lock information
        """
        return {
            'locked': self.locked_track_id is not None,
            'track_id': self.locked_track_id,
            'lock_timestamp': self.lock_timestamp,
            'frames_since_seen': self.frames_since_lock_seen,
            'occlusion_tolerance': self.occlusion_tolerance
        }
