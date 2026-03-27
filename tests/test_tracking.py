"""
Unit tests for tracking module.
"""
import pytest
from datetime import datetime

from src.modules.tracking import ByteTracker
from src.core.models import Detection, BoundingBox, TargetClass, FrameData


@pytest.fixture
def tracker():
    """Create tracker instance."""
    return ByteTracker(
        track_thresh=0.5,
        track_buffer=30,
        match_thresh=0.8
    )


def test_tracker_initialization(tracker):
    """Test tracker initializes correctly."""
    assert tracker.track_thresh == 0.5
    assert tracker.track_buffer == 30
    assert len(tracker.tracked_tracks) == 0


def test_track_creation(tracker):
    """Test track creation from detections."""
    # Create dummy detection
    detection = Detection(
        bbox=BoundingBox(x=100, y=100, w=50, h=50),
        class_name=TargetClass.PERSON,
        confidence=0.9,
        frame_id=1,
        timestamp=datetime.now()
    )
    
    frame_data = FrameData(frame_id=1, timestamp=datetime.now())
    
    # Update tracker
    tracks = tracker.update([detection], frame_data)
    
    # Should create one track
    assert len(tracks) == 1
    assert tracks[0].class_name == TargetClass.PERSON


def test_track_persistence(tracker):
    """Test track persists across frames."""
    frame_data = FrameData(frame_id=1, timestamp=datetime.now())
    
    # Frame 1: Create track
    det1 = Detection(
        bbox=BoundingBox(x=100, y=100, w=50, h=50),
        class_name=TargetClass.CAR,
        confidence=0.9,
        frame_id=1,
        timestamp=datetime.now()
    )
    tracks1 = tracker.update([det1], frame_data)
    track_id = tracks1[0].track_id
    
    # Frame 2: Update same track
    frame_data.frame_id = 2
    det2 = Detection(
        bbox=BoundingBox(x=105, y=105, w=50, h=50),
        class_name=TargetClass.CAR,
        confidence=0.9,
        frame_id=2,
        timestamp=datetime.now()
    )
    tracks2 = tracker.update([det2], frame_data)
    
    # Should maintain same track ID
    assert len(tracks2) == 1
    assert tracks2[0].track_id == track_id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
