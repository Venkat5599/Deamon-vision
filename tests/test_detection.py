"""
Unit tests for detection module.
"""
import pytest
import numpy as np
from datetime import datetime

from src.modules.detection import ObjectDetector
from src.core.models import FrameData


@pytest.fixture
def detector():
    """Create detector instance."""
    det = ObjectDetector(
        model_path="yolov8n.pt",
        confidence_threshold=0.5,
        device="cpu"
    )
    det.initialize()
    return det


def test_detector_initialization(detector):
    """Test detector initializes correctly."""
    assert detector.model is not None
    assert len(detector.class_names) > 0
    assert len(detector.target_class_ids) > 0


def test_detection_on_dummy_frame(detector):
    """Test detection on dummy frame."""
    # Create dummy frame
    frame = np.zeros((640, 640, 3), dtype=np.uint8)
    frame_data = FrameData(
        frame_id=1,
        timestamp=datetime.now()
    )
    
    # Run detection
    detections = detector.detect(frame, frame_data)
    
    # Should return empty list for blank frame
    assert isinstance(detections, list)


def test_detection_fps_calculation(detector):
    """Test FPS calculation."""
    frame = np.zeros((640, 640, 3), dtype=np.uint8)
    frame_data = FrameData(frame_id=1, timestamp=datetime.now())
    
    # Run multiple detections
    for i in range(5):
        detector.detect(frame, frame_data)
    
    fps = detector.get_fps()
    assert fps > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
