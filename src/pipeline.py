"""
Main pipeline orchestrator for Daemon Vision.
Coordinates all modules and manages data flow.
"""
import asyncio
import logging
from typing import Optional
from datetime import datetime
import yaml
from pathlib import Path

from .core.queue_manager import QueueManager
from .modules.sensor_ingestion import SensorDataCollector
from .modules.detection import ObjectDetector
from .modules.tracking import ByteTracker
from .modules.locking import TargetLockManager
from .modules.api import DaemonVisionAPI

logger = logging.getLogger(__name__)


class DaemonVisionPipeline:
    """Main pipeline orchestrator."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize pipeline.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
        
        # Initialize components
        self.queue_manager: Optional[QueueManager] = None
        self.sensor_collector: Optional[SensorDataCollector] = None
        self.detector: Optional[ObjectDetector] = None
        self.tracker: Optional[ByteTracker] = None
        self.lock_manager: Optional[TargetLockManager] = None
        self.api: Optional[DaemonVisionAPI] = None
        
        self.is_running = False
        self.frame_count = 0
        self.start_time: Optional[datetime] = None
        
        # Performance metrics
        self.total_detections = 0
        self.total_tracks = 0
        self.current_fps = 0.0
        self.last_fps_update = datetime.now()
    
    def _load_config(self) -> dict:
        """Load configuration from YAML file."""
        config_file = Path(self.config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"Configuration loaded from {self.config_path}")
        return config
    
    async def initialize(self):
        """Initialize all pipeline components."""
        logger.info("Initializing Daemon Vision pipeline...")
        
        # Initialize queue manager
        queue_config = self.config.get('queue', {})
        self.queue_manager = QueueManager(
            backend=queue_config.get('backend', 'asyncio'),
            redis_url=queue_config.get('redis_url'),
            max_size=queue_config.get('max_queue_size', 100)
        )
        
        # Create queues
        self.queue_manager.create_queue('frames')
        self.queue_manager.create_queue('detections')
        self.queue_manager.create_queue('tracks')
        
        # Initialize sensor collector
        sensor_config = self.config.get('sensor', {})
        self.sensor_collector = SensorDataCollector(
            video_source=sensor_config.get('video_source'),
            telemetry_source=sensor_config.get('telemetry_source'),
            fps=sensor_config.get('fps', 30),
            enable_stabilization=sensor_config.get('enable_stabilization', True),
            enable_undistortion=sensor_config.get('enable_undistortion', False),
            frame_buffer_size=sensor_config.get('frame_buffer_size', 10),
            imgsz=self.config.get('detection', {}).get('imgsz', 640)
        )
        await self.sensor_collector.initialize()
        
        # Initialize detector
        detection_config = self.config.get('detection', {})
        self.detector = ObjectDetector(
            model_path=detection_config.get('model', 'yolov8n.pt'),
            confidence_threshold=detection_config.get('confidence_threshold', 0.5),
            iou_threshold=detection_config.get('iou_threshold', 0.45),
            target_classes=detection_config.get('target_classes'),
            device=detection_config.get('device', 'cuda'),
            half_precision=detection_config.get('half_precision', True),
            imgsz=detection_config.get('imgsz', 640)
        )
        self.detector.initialize()
        
        # Initialize tracker
        tracking_config = self.config.get('tracking', {})
        self.tracker = ByteTracker(
            track_thresh=tracking_config.get('track_thresh', 0.5),
            track_buffer=tracking_config.get('track_buffer', 90),
            match_thresh=tracking_config.get('match_thresh', 0.8),
            min_box_area=tracking_config.get('min_box_area', 100),
            trajectory_history=tracking_config.get('trajectory_history', 30)
        )
        
        # Initialize lock manager
        locking_config = self.config.get('locking', {})
        self.lock_manager = TargetLockManager(
            occlusion_tolerance_frames=locking_config.get('occlusion_tolerance_frames', 90),
            priority_weights=locking_config.get('priority_weights'),
            class_priority_map=locking_config.get('class_priority_map'),
            camera_fov_h=self.config.get('coordinate_transform', {}).get('camera_fov_horizontal', 60),
            camera_fov_v=self.config.get('coordinate_transform', {}).get('camera_fov_vertical', 45),
            image_width=detection_config.get('imgsz', 640),
            image_height=detection_config.get('imgsz', 640)
        )
        
        # Initialize API
        api_config = self.config.get('api', {})
        self.api = DaemonVisionAPI(
            host=api_config.get('host', '0.0.0.0'),
            port=api_config.get('port', 8000),
            cors_origins=api_config.get('cors_origins', ['*'])
        )
        self.api.set_lock_manager(self.lock_manager)
        self.api.set_pipeline(self)  # Allow API to trigger video source changes
        
        logger.info("Pipeline initialization complete")
    
    async def run(self):
        """Run the main pipeline."""
        if not all([self.sensor_collector, self.detector, self.tracker, self.lock_manager, self.api]):
            raise RuntimeError("Pipeline not initialized. Call initialize() first.")
        
        self.is_running = True
        self.start_time = datetime.now()
        
        logger.info("Starting Daemon Vision pipeline...")
        
        # Start API server in background
        import uvicorn
        api_config = self.config.get('api', {})
        
        api_task = asyncio.create_task(
            self._run_api_server(
                api_config.get('host', '0.0.0.0'),
                api_config.get('port', 8000)
            )
        )
        
        # Start processing loop
        try:
            await self._processing_loop()
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        except Exception as e:
            logger.error(f"Pipeline error: {e}", exc_info=True)
        finally:
            self.is_running = False
            await self.shutdown()
            api_task.cancel()
    
    async def _run_api_server(self, host: str, port: int):
        """Run FastAPI server."""
        import uvicorn
        config = uvicorn.Config(
            self.api.app,
            host=host,
            port=port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
    
    async def _processing_loop(self):
        """Main processing loop - optimized for multi-target tracking."""
        logger.info("Processing loop started - Multi-target optimized")
        
        # Track last detection results for interpolation
        last_detections = []
        detection_counter = 0
        
        while self.is_running:
            # Get frame from sensor
            frame_data = await self.sensor_collector.get_frame()
            
            if frame_data is None:
                logger.info("No more frames, stopping pipeline")
                break
            
            frame, frame_metadata = frame_data
            self.frame_count += 1
            detection_counter += 1
            
            # Smart detection: Run every 2nd frame for persistent tracking
            # This gives smooth, continuous tracking for drone delivery
            if detection_counter >= 2:
                # Run full detection
                detections = self.detector.detect(frame, frame_metadata)
                last_detections = detections
                self.total_detections += len(detections)
                detection_counter = 0
            else:
                # Reuse last detections - tracker will handle prediction
                detections = last_detections
            
            # Tracking runs EVERY frame for smooth multi-target tracking
            tracks = self.tracker.update(detections, frame_metadata)
            self.total_tracks = len(tracks)
            
            # Update lock (lightweight)
            locked_track = self.lock_manager.update_lock(tracks)
            
            # Broadcast every 2nd frame for smooth video (balance speed/smoothness)
            if self.frame_count % 2 == 0:
                # Non-blocking broadcast
                asyncio.create_task(self.api.broadcast_tracks(tracks, frame))
            
            # Log progress
            if self.frame_count % 120 == 0:
                self._log_metrics()
        
        logger.info("Processing loop ended")
    
    def _log_metrics(self):
        """Log performance metrics."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        pipeline_fps = self.frame_count / elapsed if elapsed > 0 else 0
        self.current_fps = pipeline_fps  # Store for API access
        
        logger.info(
            f"Frame {self.frame_count} | "
            f"Pipeline FPS: {pipeline_fps:.2f} | "
            f"Detection FPS: {self.detector.get_fps():.2f} | "
            f"Active tracks: {self.total_tracks} | "
            f"Total detections: {self.total_detections}"
        )
    
    async def shutdown(self):
        """Shutdown pipeline gracefully."""
        logger.info("Shutting down pipeline...")
        
        self.is_running = False
        
        if self.sensor_collector:
            await self.sensor_collector.close()
        
        if self.queue_manager:
            await self.queue_manager.close()
        
        # Final metrics
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            logger.info(
                f"Pipeline stopped. Processed {self.frame_count} frames in {elapsed:.2f}s "
                f"({self.frame_count / elapsed:.2f} FPS)"
            )
        
        logger.info("Shutdown complete")
    
    async def switch_video_source(self, new_source):
        """
        Switch to a new video source dynamically.
        
        Args:
            new_source: Path to video file or camera index
        """
        logger.info(f"Switching video source to: {new_source}")
        
        # Close current sensor
        if self.sensor_collector:
            await self.sensor_collector.close()
        
        # Create new sensor with new source
        sensor_config = self.config.get('sensor', {})
        self.sensor_collector = SensorDataCollector(
            video_source=new_source,
            telemetry_source=sensor_config.get('telemetry_source'),
            fps=sensor_config.get('fps', 30),
            enable_stabilization=sensor_config.get('enable_stabilization', True),
            enable_undistortion=sensor_config.get('enable_undistortion', False),
            frame_buffer_size=sensor_config.get('frame_buffer_size', 10),
            imgsz=self.config.get('detection', {}).get('imgsz', 640)
        )
        await self.sensor_collector.initialize()
        
        # Reset counters
        self.frame_count = 0
        self.start_time = datetime.now()
        
        logger.info("Video source switched successfully")
