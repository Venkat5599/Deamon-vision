"""
Unit tests for API module.
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from src.modules.api import DaemonVisionAPI
from src.modules.locking import TargetLockManager
from src.core.models import TrackObject, BoundingBox, TargetClass, Velocity


@pytest.fixture
def api():
    """Create API instance."""
    api = DaemonVisionAPI()
    lock_manager = TargetLockManager()
    api.set_lock_manager(lock_manager)
    return api


@pytest.fixture
def client(api):
    """Create test client."""
    return TestClient(api.app)


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_get_tracks_empty(client):
    """Test getting tracks when none exist."""
    response = client.get("/tracks")
    assert response.status_code == 200
    data = response.json()
    assert "tracks" in data
    assert len(data["tracks"]) == 0


def test_get_tracks_with_data(client, api):
    """Test getting tracks with data."""
    # Add dummy track
    track = TrackObject(
        track_id=1,
        class_name=TargetClass.PERSON,
        confidence=0.9,
        bbox=BoundingBox(x=100, y=100, w=50, h=50),
        velocity=Velocity(vx=1.0, vy=0.5),
        trajectory=[],
        last_seen=datetime.now()
    )
    api.current_tracks = [track]
    
    response = client.get("/tracks")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tracks"]) == 1
    assert data["tracks"][0]["track_id"] == 1


def test_lock_nonexistent_track(client):
    """Test locking non-existent track."""
    response = client.post("/lock/999")
    assert response.status_code == 404


def test_lock_existing_track(client, api):
    """Test locking existing track."""
    # Add dummy track
    track = TrackObject(
        track_id=1,
        class_name=TargetClass.CAR,
        confidence=0.9,
        bbox=BoundingBox(x=100, y=100, w=50, h=50),
        trajectory=[],
        last_seen=datetime.now()
    )
    api.current_tracks = [track]
    
    response = client.post("/lock/1")
    assert response.status_code == 200
    data = response.json()
    assert data["locked"] is True
    assert data["track_id"] == 1


def test_unlock_target(client):
    """Test unlocking target."""
    response = client.delete("/lock")
    assert response.status_code == 200
    data = response.json()
    assert data["locked"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
