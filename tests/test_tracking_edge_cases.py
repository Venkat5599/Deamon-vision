"""
Comprehensive tests for Module 3 edge cases:
- Occlusion handling
- Target re-entry
- Track expiration (>N frames)
"""
import pytest
from datetime import datetime, timedelta
from src.modules.tracking import ByteTracker
from src.core.models import Detection, BoundingBox, FrameData, TargetClass


@pytest.fixture
def tracker():
    """Create ByteTracker with production settings."""
    return ByteTracker(
        track_thresh=0.35,
        track_buffer=300,  # 10 seconds at 30fps
        match_thresh=0.65,
        min_box_area=30,
        trajectory_history=300
    )


@pytest.fixture
def sample_detection():
    """Create a sample detection."""
    return Detection(
        bbox=BoundingBox(x=100, y=100, w=50, h=50),
        confidence=0.8,
        class_name=TargetClass.CAR,
        timestamp=datetime.now()
    )


@pytest.fixture
def frame_data():
    """Create sample frame metadata."""
    return FrameData(
        frame_id=0,
        timestamp=datetime.now(),
        telemetry=None
    )


class TestOcclusionHandling:
    """Test occlusion scenarios where target is temporarily hidden."""
    
    def test_short_occlusion_3_seconds(self, tracker, sample_detection, frame_data):
        """
        Test: Object occluded for 3 seconds (90 frames)
        Expected: Same track ID maintained, track visible throughout
        """
        # Initial detection
        tracks = tracker.update([sample_detection], frame_data)
        assert len(tracks) == 1
        original_id = tracks[0].track_id
        
        # Simulate 3-second occlusion (90 frames at 30fps)
        for i in range(90):
            frame_data.frame_id = i + 1
            frame_data.timestamp += timedelta(seconds=1/30)
            tracks = tracker.update([], frame_data)  # No detections
            
            # Track should still be visible (using prediction)
            assert len(tracks) == 1, f"Track lost at frame {i+1}"
            assert tracks[0].track_id == original_id
            assert tracks[0].frames_since_update == i + 1
        
        # Object reappears
        frame_data.frame_id = 91
        frame_data.timestamp += timedelta(seconds=1/30)
        tracks = tracker.update([sample_detection], frame_data)
        
        # Should recover with same ID
        assert len(tracks) == 1
        assert tracks[0].track_id == original_id
        assert tracks[0].frames_since_update == 0
    
    def test_long_occlusion_8_seconds(self, tracker, sample_detection, frame_data):
        """
        Test: Object occluded for 8 seconds (240 frames)
        Expected: Track maintained, ID preserved
        """
        # Initial detection
        tracks = tracker.update([sample_detection], frame_data)
        original_id = tracks[0].track_id
        
        # Simulate 8-second occlusion (240 frames)
        for i in range(240):
            frame_data.frame_id = i + 1
            frame_data.timestamp += timedelta(seconds=1/30)
            tracks = tracker.update([], frame_data)
        
        # Object reappears at same location
        frame_data.frame_id = 241
        frame_data.timestamp += timedelta(seconds=1/30)
        tracks = tracker.update([sample_detection], frame_data)
        
        # Should recover with same ID
        assert len(tracks) == 1
        assert tracks[0].track_id == original_id
    
    def test_maximum_occlusion_10_seconds(self, tracker, sample_detection, frame_data):
        """
        Test: Object occluded for exactly 10 seconds (300 frames)
        Expected: Track at edge of buffer, should recover
        """
        # Initial detection
        tracks = tracker.update([sample_detection], frame_data)
        original_id = tracks[0].track_id
        
        # Simulate 10-second occlusion (300 frames)
        for i in range(299):  # 299 frames = just under threshold
            frame_data.frame_id = i + 1
            frame_data.timestamp += timedelta(seconds=1/30)
            tracks = tracker.update([], frame_data)
        
        # Object reappears just before expiration
        frame_data.frame_id = 300
        frame_data.timestamp += timedelta(seconds=1/30)
        tracks = tracker.update([sample_detection], frame_data)
        
        # Should recover with same ID (within buffer)
        assert len(tracks) == 1
        assert tracks[0].track_id == original_id
    
    def test_kalman_prediction_during_occlusion(self, tracker, frame_data):
        """
        Test: Verify Kalman filter predicts position during occlusion
        Expected: Bounding box continues to move based on velocity
        """
        # Create moving object (3 detections to establish velocity)
        detections = [
            Detection(
                bbox=BoundingBox(x=100 + i*10, y=100, w=50, h=50),
                confidence=0.8,
                class_name=TargetClass.CAR,
                timestamp=frame_data.timestamp
            )
            for i in range(3)
        ]
        
        # Establish track with velocity
        for i, det in enumerate(detections):
            frame_data.frame_id = i
            frame_data.timestamp += timedelta(seconds=1/30)
            tracks = tracker.update([det], frame_data)
        
        original_id = tracks[0].track_id
        last_x = tracks[0].bbox.x
        
        # Simulate occlusion - position should continue moving
        for i in range(10):
            frame_data.frame_id = 3 + i
            frame_data.timestamp += timedelta(seconds=1/30)
            tracks = tracker.update([], frame_data)
            
            # Predicted position should move forward
            assert tracks[0].bbox.x > last_x, "Kalman prediction not working"
            last_x = tracks[0].bbox.x


class TestTargetReentry:
    """Test scenarios where object leaves and returns to frame."""
    
    def test_reentry_within_buffer_5_seconds(self, tracker, sample_detection, frame_data):
        """
        Test: Object exits and returns within 5 seconds (150 frames)
        Expected: Same track ID assigned
        """
        # Initial detection
        tracks = tracker.update([sample_detection], frame_data)
        original_id = tracks[0].track_id
        
        # Object exits frame (150 frames = 5 seconds)
        for i in range(150):
            frame_data.frame_id = i + 1
            frame_data.timestamp += timedelta(seconds=1/30)
            tracks = tracker.update([], frame_data)
        
        # Object re-enters at similar location
        frame_data.frame_id = 151
        frame_data.timestamp += timedelta(seconds=1/30)
        reentry_detection = Detection(
            bbox=BoundingBox(x=105, y=105, w=50, h=50),  # Slightly moved
            confidence=0.8,
            class_name=TargetClass.CAR,
            timestamp=frame_data.timestamp
        )
        tracks = tracker.update([reentry_detection], frame_data)
        
        # Should re-associate with same ID
        assert len(tracks) == 1
        assert tracks[0].track_id == original_id
    
    def test_reentry_after_buffer_expiration(self, tracker, sample_detection, frame_data):
        """
        Test: Object exits and returns after 11 seconds (330 frames)
        Expected: New track ID assigned
        """
        # Initial detection
        tracks = tracker.update([sample_detection], frame_data)
        original_id = tracks[0].track_id
        
        # Object exits frame (330 frames = 11 seconds, exceeds buffer)
        for i in range(330):
            frame_data.frame_id = i + 1
            frame_data.timestamp += timedelta(seconds=1/30)
            tracks = tracker.update([], frame_data)
        
        # Object re-enters
        frame_data.frame_id = 331
        frame_data.timestamp += timedelta(seconds=1/30)
        tracks = tracker.update([sample_detection], frame_data)
        
        # Should get NEW track ID (old track expired)
        assert len(tracks) == 1
        assert tracks[0].track_id != original_id
    
    def test_reentry_different_location(self, tracker, sample_detection, frame_data):
        """
        Test: Object re-enters at very different location
        Expected: New track ID (IoU matching fails)
        """
        # Initial detection at (100, 100)
        tracks = tracker.update([sample_detection], frame_data)
        original_id = tracks[0].track_id
        
        # Brief absence (30 frames)
        for i in range(30):
            frame_data.frame_id = i + 1
            frame_data.timestamp += timedelta(seconds=1/30)
            tracks = tracker.update([], frame_data)
        
        # Re-enters at completely different location (500, 500)
        frame_data.frame_id = 31
        frame_data.timestamp += timedelta(seconds=1/30)
        far_detection = Detection(
            bbox=BoundingBox(x=500, y=500, w=50, h=50),
            confidence=0.8,
            class_name=TargetClass.CAR,
            timestamp=frame_data.timestamp
        )
        tracks = tracker.update([far_detection], frame_data)
        
        # Should get new ID (IoU too low for matching)
        assert len(tracks) == 1
        assert tracks[0].track_id != original_id


class TestTrackExpiration:
    """Test track removal after N frames without detection."""
    
    def test_track_expires_after_300_frames(self, tracker, sample_detection, frame_data):
        """
        Test: Track expires after exactly 300 frames (10 seconds)
        Expected: Track removed, ID available for reuse
        """
        # Initial detection
        tracks = tracker.update([sample_detection], frame_data)
        original_id = tracks[0].track_id
        
        # No detections for 300 frames
        for i in range(300):
            frame_data.frame_id = i + 1
            frame_data.timestamp += timedelta(seconds=1/30)
            tracks = tracker.update([], frame_data)
        
        # After 300 frames, track should still exist (at threshold)
        # But at frame 301, it should be removed
        frame_data.frame_id = 301
        frame_data.timestamp += timedelta(seconds=1/30)
        tracks = tracker.update([], frame_data)
        
        # Track should be removed
        assert len(tracks) == 0
        
        # New detection should get new ID (or reuse old one)
        frame_data.frame_id = 302
        frame_data.timestamp += timedelta(seconds=1/30)
        tracks = tracker.update([sample_detection], frame_data)
        assert len(tracks) == 1
        # ID may be reused or new, but track is fresh
        assert tracks[0].frames_since_update == 0
    
    def test_multiple_tracks_independent_expiration(self, tracker, frame_data):
        """
        Test: Multiple tracks expire independently
        Expected: Each track expires based on its own timer
        """
        # Create 3 tracks at different times
        track_ids = []
        for i in range(3):
            frame_data.frame_id = i * 50
            frame_data.timestamp += timedelta(seconds=i * 50 / 30)
            detection = Detection(
                bbox=BoundingBox(x=100 + i*100, y=100, w=50, h=50),
                confidence=0.8,
                class_name=TargetClass.CAR,
                timestamp=frame_data.timestamp
            )
            tracks = tracker.update([detection], frame_data)
            track_ids.append(tracks[-1].track_id)
        
        # Advance 350 frames (all tracks should expire)
        for i in range(350):
            frame_data.frame_id = 150 + i
            frame_data.timestamp += timedelta(seconds=1/30)
            tracks = tracker.update([], frame_data)
        
        # All tracks should be expired
        assert len(tracks) == 0


class TestTrajectoryHistory:
    """Test trajectory history requirements (min 30, max 300 frames)."""
    
    def test_trajectory_minimum_30_frames(self, tracker, frame_data):
        """
        Test: Trajectory contains at least 30 points after 30 frames
        Expected: trajectory list has 30 entries
        """
        # Create 30 detections
        for i in range(30):
            frame_data.frame_id = i
            frame_data.timestamp += timedelta(seconds=1/30)
            detection = Detection(
                bbox=BoundingBox(x=100 + i, y=100, w=50, h=50),
                confidence=0.8,
                class_name=TargetClass.CAR,
                timestamp=frame_data.timestamp
            )
            tracks = tracker.update([detection], frame_data)
        
        # Check trajectory length
        assert len(tracks) == 1
        assert len(tracks[0].trajectory) >= 30
    
    def test_trajectory_maximum_300_frames(self, tracker, frame_data):
        """
        Test: Trajectory capped at 300 points
        Expected: trajectory list has exactly 300 entries after 400 frames
        """
        # Create 400 detections
        for i in range(400):
            frame_data.frame_id = i
            frame_data.timestamp += timedelta(seconds=1/30)
            detection = Detection(
                bbox=BoundingBox(x=100 + i, y=100, w=50, h=50),
                confidence=0.8,
                class_name=TargetClass.CAR,
                timestamp=frame_data.timestamp
            )
            tracks = tracker.update([detection], frame_data)
        
        # Check trajectory length is capped
        assert len(tracks) == 1
        assert len(tracks[0].trajectory) == 300  # Capped at max
    
    def test_velocity_calculation(self, tracker, frame_data):
        """
        Test: Velocity vector calculated from trajectory
        Expected: Non-zero velocity for moving object
        """
        # Create moving object (10 pixels per frame)
        for i in range(50):
            frame_data.frame_id = i
            frame_data.timestamp += timedelta(seconds=1/30)
            detection = Detection(
                bbox=BoundingBox(x=100 + i*10, y=100, w=50, h=50),
                confidence=0.8,
                class_name=TargetClass.CAR,
                timestamp=frame_data.timestamp
            )
            tracks = tracker.update([detection], frame_data)
        
        # Check velocity is calculated
        assert len(tracks) == 1
        assert tracks[0].velocity is not None
        assert tracks[0].velocity.vx > 0  # Moving right
        assert abs(tracks[0].velocity.vy) < 1  # Not moving vertically


class TestMultiTargetScenarios:
    """Test complex multi-target scenarios."""
    
    def test_multiple_targets_simultaneous_occlusion(self, tracker, frame_data):
        """
        Test: Multiple targets occluded simultaneously
        Expected: All tracks maintained independently
        """
        # Create 5 targets
        detections = [
            Detection(
                bbox=BoundingBox(x=100 + i*100, y=100, w=50, h=50),
                confidence=0.8,
                class_name=TargetClass.CAR,
                timestamp=frame_data.timestamp
            )
            for i in range(5)
        ]
        
        tracks = tracker.update(detections, frame_data)
        assert len(tracks) == 5
        original_ids = [t.track_id for t in tracks]
        
        # All targets occluded for 5 seconds (150 frames)
        for i in range(150):
            frame_data.frame_id = i + 1
            frame_data.timestamp += timedelta(seconds=1/30)
            tracks = tracker.update([], frame_data)
        
        # All targets reappear
        frame_data.frame_id = 151
        frame_data.timestamp += timedelta(seconds=1/30)
        tracks = tracker.update(detections, frame_data)
        
        # All should recover with same IDs
        assert len(tracks) == 5
        recovered_ids = [t.track_id for t in tracks]
        assert set(original_ids) == set(recovered_ids)


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
