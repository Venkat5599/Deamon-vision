"""
Module 2: Multi-Object Detection
YOLOv8-based real-time object detection for aerial targets.
"""
import cv2
import numpy as np
import torch
from typing import List, Optional
from datetime import datetime
import logging

from ultralytics import YOLO
from ..core.models import Detection, BoundingBox, TargetClass, FrameData

logger = logging.getLogger(__name__)


class ObjectDetector:
    """YOLOv8-based object detector for aerial surveillance."""
    
    def __init__(
        self,
        model_path: str = "yolov8n.pt",
        confidence_threshold: float = 0.25,
        iou_threshold: float = 0.5,
        target_classes: Optional[List[str]] = None,
        device: str = "cuda",
        half_precision: bool = False,
        imgsz: int = 640,
        max_det: int = 100
    ):
        """
        Initialize object detector.
        
        Args:
            model_path: Path to YOLO model weights
            confidence_threshold: Minimum confidence for detections
            iou_threshold: IoU threshold for NMS
            target_classes: List of target class names to detect
            device: Device to run inference on ("cuda" or "cpu")
            half_precision: Use FP16 for faster inference
            imgsz: Input image size
            max_det: Maximum detections per image
        """
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.target_classes = target_classes or [
            "person", "car", "truck", "bus", "motorcycle", "bicycle", "airplane"
        ]
        self.device = device
        self.half_precision = half_precision and device == "cuda"
        self.imgsz = imgsz
        self.max_det = max_det
        
        self.model: Optional[YOLO] = None
        self.class_names: dict = {}
        self.target_class_ids: List[int] = []
        
        # Performance metrics
        self.detections_count = 0
        self.inference_times: List[float] = []
    
    def initialize(self):
        """Initialize YOLO model."""
        logger.info(f"Loading YOLO model: {self.model_path}")
        
        try:
            self.model = YOLO(self.model_path)
            
            # Move to device
            if self.device == "cuda" and torch.cuda.is_available():
                self.model.to("cuda")
                # Disable FP16 to avoid dtype mismatch issues
                self.half_precision = False
                logger.info(f"Model loaded on CUDA (FP32 for stability)")
            else:
                self.model.to("cpu")
                self.half_precision = False
                logger.info("Model loaded on CPU")
            
            # Get class names
            self.class_names = self.model.names
            
            # Map target classes to IDs
            self.target_class_ids = []
            for class_name in self.target_classes:
                for class_id, name in self.class_names.items():
                    if name.lower() == class_name.lower():
                        self.target_class_ids.append(class_id)
                        break
            
            logger.info(f"Target classes: {self.target_classes}")
            logger.info(f"Target class IDs: {self.target_class_ids}")
            
            # Warmup
            dummy_img = np.zeros((self.imgsz, self.imgsz, 3), dtype=np.uint8)
            _ = self.model.predict(
                dummy_img,
                conf=self.confidence_threshold,
                iou=self.iou_threshold,
                verbose=False,
                half=False  # Explicitly disable FP16
            )
            logger.info("Model warmup complete")
            
        except Exception as e:
            logger.error(f"Failed to initialize detector: {e}")
            raise
    
    def detect(
        self,
        frame: np.ndarray,
        frame_data: FrameData
    ) -> List[Detection]:
        """
        Detect objects in frame.
        
        Args:
            frame: Input frame (BGR)
            frame_data: Frame metadata
        
        Returns:
            List of Detection objects
        """
        if self.model is None:
            raise RuntimeError("Detector not initialized")
        
        start_time = datetime.now()
        
        # Run inference with optimized parameters
        results = self.model.predict(
            frame,
            conf=self.confidence_threshold,
            iou=self.iou_threshold,
            classes=self.target_class_ids if self.target_class_ids else None,
            verbose=False,
            device=self.device,
            half=False,  # Disable FP16 for stability
            max_det=self.max_det,  # Limit max detections
            agnostic_nms=False  # Class-specific NMS for better multi-target
        )
        
        # Parse results
        detections = []
        
        if len(results) > 0:
            result = results[0]
            boxes = result.boxes
            
            if boxes is not None and len(boxes) > 0:
                for box in boxes:
                    # Get box coordinates (xyxy format)
                    xyxy = box.xyxy[0].cpu().numpy()
                    x1, y1, x2, y2 = xyxy
                    
                    # Convert to xywh
                    x, y, w, h = x1, y1, x2 - x1, y2 - y1
                    
                    # Get class and confidence
                    class_id = int(box.cls[0].item())
                    confidence = float(box.conf[0].item())
                    class_name = self.class_names[class_id]
                    
                    # Map to TargetClass enum
                    try:
                        target_class = TargetClass(class_name.lower())
                    except ValueError:
                        # Skip if not in target classes
                        continue
                    
                    # Create detection
                    detection = Detection(
                        bbox=BoundingBox(x=x, y=y, w=w, h=h),
                        class_name=target_class,
                        confidence=confidence,
                        frame_id=frame_data.frame_id,
                        timestamp=frame_data.timestamp
                    )
                    
                    detections.append(detection)
        
        # Update metrics
        inference_time = (datetime.now() - start_time).total_seconds() * 1000
        self.inference_times.append(inference_time)
        self.detections_count += len(detections)
        
        # Keep only last 100 inference times
        if len(self.inference_times) > 100:
            self.inference_times = self.inference_times[-100:]
        
        return detections
    
    def get_avg_inference_time(self) -> float:
        """Get average inference time in milliseconds."""
        if not self.inference_times:
            return 0.0
        return sum(self.inference_times) / len(self.inference_times)
    
    def get_fps(self) -> float:
        """Get average detection FPS."""
        avg_time = self.get_avg_inference_time()
        return 1000.0 / avg_time if avg_time > 0 else 0.0
    
    def draw_detections(
        self,
        frame: np.ndarray,
        detections: List[Detection]
    ) -> np.ndarray:
        """
        Draw detections on frame for visualization.
        
        Args:
            frame: Input frame
            detections: List of detections
        
        Returns:
            Frame with drawn detections
        """
        output = frame.copy()
        
        for det in detections:
            x1, y1, x2, y2 = det.bbox.to_xyxy()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Draw box
            color = (0, 255, 0)
            cv2.rectangle(output, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"{det.class_name.value} {det.confidence:.2f}"
            (label_w, label_h), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
            )
            cv2.rectangle(
                output,
                (x1, y1 - label_h - 10),
                (x1 + label_w, y1),
                color,
                -1
            )
            cv2.putText(
                output,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                1
            )
        
        return output
