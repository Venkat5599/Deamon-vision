"""
Core data models for Daemon Vision pipeline.
Pydantic models for type safety and validation.
"""
from datetime import datetime
from typing import List, Optional, Tuple
from enum import Enum
from pydantic import BaseModel, Field
import numpy as np


class TargetClass(str, Enum):
    """Supported target classes."""
    PERSON = "person"
    CAR = "car"
    TRUCK = "truck"
    BUS = "bus"
    MOTORCYCLE = "motorcycle"
    BICYCLE = "bicycle"
    AIRPLANE = "airplane"


class BoundingBox(BaseModel):
    """Bounding box in image coordinates."""
    x: float = Field(..., description="Top-left x coordinate")
    y: float = Field(..., description="Top-left y coordinate")
    w: float = Field(..., description="Width")
    h: float = Field(..., description="Height")
    
    @property
    def center(self) -> Tuple[float, float]:
        """Get center point of bbox."""
        return (self.x + self.w / 2, self.y + self.h / 2)
    
    @property
    def area(self) -> float:
        """Get bbox area."""
        return self.w * self.h
    
    def to_xyxy(self) -> Tuple[float, float, float, float]:
        """Convert to (x1, y1, x2, y2) format."""
        return (self.x, self.y, self.x + self.w, self.y + self.h)


class GroundCoordinate(BaseModel):
    """Geographic coordinate."""
    lat: float = Field(..., description="Latitude in degrees")
    lon: float = Field(..., description="Longitude in degrees")
    alt: Optional[float] = Field(None, description="Altitude in meters")


class Velocity(BaseModel):
    """2D velocity vector."""
    vx: float = Field(..., description="Velocity in x direction (m/s)")
    vy: float = Field(..., description="Velocity in y direction (m/s)")
    
    @property
    def magnitude(self) -> float:
        """Get velocity magnitude."""
        return float(np.sqrt(self.vx**2 + self.vy**2))


class Detection(BaseModel):
    """Single object detection from detector."""
    bbox: BoundingBox
    class_name: TargetClass
    confidence: float = Field(..., ge=0.0, le=1.0)
    frame_id: int
    timestamp: datetime


class TrajectoryPoint(BaseModel):
    """Single point in trajectory history."""
    x: float
    y: float
    timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TrackObject(BaseModel):
    """Tracked object with persistent ID."""
    track_id: int
    class_name: TargetClass
    confidence: float
    bbox: BoundingBox
    ground_coord: Optional[GroundCoordinate] = None
    velocity: Optional[Velocity] = None
    trajectory: List[TrajectoryPoint] = Field(default_factory=list)
    last_seen: datetime
    frames_since_update: int = 0
    is_locked: bool = False
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class GimbalCommand(BaseModel):
    """Gimbal pointing command."""
    azimuth: float = Field(..., description="Azimuth delta in degrees")
    elevation: float = Field(..., description="Elevation delta in degrees")


class LockResponse(BaseModel):
    """Response for lock command."""
    track_id: int
    locked: bool
    gimbal_delta: Optional[GimbalCommand] = None
    timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TrackListResponse(BaseModel):
    """Response for listing all tracks."""
    tracks: List[TrackObject]
    timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TrajectoryResponse(BaseModel):
    """Response for trajectory query."""
    track_id: int
    trajectory: List[TrajectoryPoint]
    predicted_position: Optional[TrajectoryPoint] = None
    velocity: Optional[Velocity] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TelemetryData(BaseModel):
    """Telemetry data from platform."""
    timestamp: datetime
    gps: GroundCoordinate
    altitude: float = Field(..., description="Altitude above ground in meters")
    gimbal_azimuth: float = Field(..., description="Gimbal azimuth in degrees")
    gimbal_elevation: float = Field(..., description="Gimbal elevation in degrees")
    heading: float = Field(..., description="Platform heading in degrees")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class FrameData(BaseModel):
    """Processed frame with metadata."""
    frame_id: int
    timestamp: datetime
    telemetry: Optional[TelemetryData] = None
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
