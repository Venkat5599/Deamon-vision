"""
Module 1: Sensor Data Ingestion & Preprocessing
Handles video stream input, telemetry synchronization, and frame preprocessing.
"""
import cv2
import numpy as np
import asyncio
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from pathlib import Path
import logging

from ..core.models import TelemetryData, FrameData
from ..core.utils import stabilize_frame_ecc, adaptive_resize, timestamp_sync

logger = logging.getLogger(__name__)


class SensorDataCollector:
    """Collects and preprocesses video and telemetry data."""
    
    def __init__(
        self,
        video_source: str,
        telemetry_source: Optional[str] = None,
        fps: int = 30,
        enable_stabilization: bool = True,
        enable_undistortion: bool = False,
        frame_buffer_size: int = 10,
        imgsz: int = 640
    ):
        """
        Initialize sensor data collector.
        
        Args:
            video_source: Path to video file or RTSP URL
            telemetry_source: Path to telemetry JSON file
            fps: Target frame rate
            enable_stabilization: Enable ECC stabilization
            enable_undistortion: Enable lens undistortion
            frame_buffer_size: Size of frame buffer
            imgsz: Target image size for processing
        """
        self.video_source = video_source
        self.telemetry_source = telemetry_source
        self.target_fps = fps
        self.enable_stabilization = enable_stabilization
        self.enable_undistortion = enable_undistortion
        self.frame_buffer_size = frame_buffer_size
        self.imgsz = imgsz
        
        self.cap: Optional[cv2.VideoCapture] = None
        self.telemetry_data: List[Dict] = []
        self.frame_count = 0
        self.prev_frame: Optional[np.ndarray] = None
        self.prev_transform: Optional[np.ndarray] = None
        self.camera_matrix: Optional[np.ndarray] = None
        self.dist_coeffs: Optional[np.ndarray] = None
        self.is_running = False
        
        # Performance metrics
        self.frames_processed = 0
        self.start_time: Optional[datetime] = None
    
    async def initialize(self):
        """Initialize video capture and load telemetry."""
        logger.info(f"Initializing sensor data collector: {self.video_source}")
        
        # Initialize video capture
        self.cap = cv2.VideoCapture(self.video_source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open video source: {self.video_source}")
        
        # Get video properties
        self.video_fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        logger.info(
            f"Video properties: {self.video_width}x{self.video_height} @ {self.video_fps} FPS, "
            f"{self.total_frames} frames"
        )
        
        # Load telemetry data
        if self.telemetry_source and Path(self.telemetry_source).exists():
            await self._load_telemetry()
        else:
            logger.warning("No telemetry data provided, using simulated data")
            self._generate_simulated_telemetry()
        
        # Initialize camera calibration (if needed)
        if self.enable_undistortion:
            self._init_camera_calibration()
        
        self.is_running = True
        self.start_time = datetime.now()
        logger.info("Sensor data collector initialized successfully")
    
    async def _load_telemetry(self):
        """Load telemetry data from JSON file."""
        try:
            with open(self.telemetry_source, 'r') as f:
                data = json.load(f)
            
            # Parse telemetry entries
            for entry in data:
                self.telemetry_data.append({
                    'timestamp': datetime.fromisoformat(entry['timestamp']),
                    'gps': {
                        'lat': entry['gps']['lat'],
                        'lon': entry['gps']['lon']
                    },
                    'altitude': entry['altitude'],
                    'gimbal_azimuth': entry['gimbal_azimuth'],
                    'gimbal_elevation': entry['gimbal_elevation'],
                    'heading': entry.get('heading', 0.0)
                })
            
            logger.info(f"Loaded {len(self.telemetry_data)} telemetry entries")
        except Exception as e:
            logger.error(f"Failed to load telemetry: {e}")
            self._generate_simulated_telemetry()
    
    def _generate_simulated_telemetry(self):
        """Generate simulated telemetry data for testing."""
        logger.info("Generating simulated telemetry data")
        
        # Simulate 60 seconds of telemetry at 10 Hz
        base_time = datetime.now()
        base_lat = -6.2088  # Jakarta
        base_lon = 106.8456
        
        for i in range(600):
            self.telemetry_data.append({
                'timestamp': base_time + timedelta(milliseconds=i * 100),
                'gps': {
                    'lat': base_lat + np.random.normal(0, 0.0001),
                    'lon': base_lon + np.random.normal(0, 0.0001)
                },
                'altitude': 150.0 + np.random.normal(0, 5.0),
                'gimbal_azimuth': 0.0 + np.random.normal(0, 2.0),
                'gimbal_elevation': -45.0 + np.random.normal(0, 1.0),
                'heading': 90.0 + np.random.normal(0, 2.0)
            })
    
    def _init_camera_calibration(self):
        """Initialize camera calibration parameters."""
        # Placeholder - in production, load from calibration file
        self.camera_matrix = np.array([
            [self.video_width, 0, self.video_width / 2],
            [0, self.video_width, self.video_height / 2],
            [0, 0, 1]
        ], dtype=np.float32)
        
        self.dist_coeffs = np.zeros((5, 1), dtype=np.float32)
        logger.info("Camera calibration initialized (placeholder)")
    
    async def get_frame(self) -> Optional[Tuple[np.ndarray, FrameData]]:
        """
        Get next preprocessed frame with synchronized telemetry.
        
        Returns:
            (frame, frame_data) tuple or None if no more frames
        """
        if not self.is_running or not self.cap:
            return None
        
        # Read frame
        ret, frame = self.cap.read()
        if not ret:
            # Loop video - restart from beginning
            logger.info("End of video - looping back to start")
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.frame_count = 0
            ret, frame = self.cap.read()
            if not ret:
                logger.error("Failed to restart video")
                return None
        
        self.frame_count += 1
        frame_timestamp = datetime.now()
        
        # Undistort frame (if enabled)
        if self.enable_undistortion and self.camera_matrix is not None:
            frame = cv2.undistort(frame, self.camera_matrix, self.dist_coeffs)
        
        # Stabilize frame (if enabled)
        if self.enable_stabilization and self.prev_frame is not None:
            frame, self.prev_transform = stabilize_frame_ecc(
                frame, self.prev_frame, self.prev_transform
            )
        
        # Find synchronized telemetry
        telemetry_dict = timestamp_sync(frame_timestamp, self.telemetry_data)
        telemetry = None
        
        if telemetry_dict:
            telemetry = TelemetryData(
                timestamp=telemetry_dict['timestamp'],
                gps=telemetry_dict['gps'],
                altitude=telemetry_dict['altitude'],
                gimbal_azimuth=telemetry_dict['gimbal_azimuth'],
                gimbal_elevation=telemetry_dict['gimbal_elevation'],
                heading=telemetry_dict['heading']
            )
            
            # Adaptive resize based on altitude
            frame = adaptive_resize(
                frame,
                telemetry.altitude,
                base_size=self.imgsz
            )
        else:
            # Default resize
            frame = cv2.resize(frame, (self.imgsz, self.imgsz))
        
        # Store for next stabilization
        self.prev_frame = frame.copy()
        
        # Create frame data
        frame_data = FrameData(
            frame_id=self.frame_count,
            timestamp=frame_timestamp,
            telemetry=telemetry
        )
        
        self.frames_processed += 1
        
        # Rate limiting to target FPS
        if self.video_fps > self.target_fps:
            await asyncio.sleep(1.0 / self.target_fps)
        
        return frame, frame_data
    
    def get_fps(self) -> float:
        """Get current processing FPS."""
        if self.start_time is None or self.frames_processed == 0:
            return 0.0
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return self.frames_processed / elapsed if elapsed > 0 else 0.0
    
    async def close(self):
        """Release resources."""
        self.is_running = False
        if self.cap:
            self.cap.release()
            logger.info("Video capture released")
        
        # Log final stats
        fps = self.get_fps()
        logger.info(f"Sensor collector closed. Processed {self.frames_processed} frames at {fps:.2f} FPS")
