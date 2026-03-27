"""
Utility functions for coordinate transforms, geometry, and helpers.
"""
import math
import numpy as np
from typing import Tuple, Optional
from datetime import datetime
import cv2


def flat_earth_projection(
    pixel_x: float,
    pixel_y: float,
    image_width: int,
    image_height: int,
    platform_lat: float,
    platform_lon: float,
    altitude: float,
    gimbal_azimuth: float,
    gimbal_elevation: float,
    camera_fov_h: float = 60.0,
    camera_fov_v: float = 45.0
) -> Tuple[float, float]:
    """
    Convert pixel coordinates to ground coordinates using flat-earth approximation.
    
    Args:
        pixel_x, pixel_y: Pixel coordinates in image
        image_width, image_height: Image dimensions
        platform_lat, platform_lon: Platform GPS coordinates
        altitude: Altitude above ground in meters
        gimbal_azimuth: Gimbal azimuth in degrees (0 = North, clockwise)
        gimbal_elevation: Gimbal elevation in degrees (negative = down)
        camera_fov_h, camera_fov_v: Camera field of view in degrees
    
    Returns:
        (latitude, longitude) of ground point
    """
    # Normalize pixel coordinates to [-1, 1]
    norm_x = (pixel_x - image_width / 2) / (image_width / 2)
    norm_y = (pixel_y - image_height / 2) / (image_height / 2)
    
    # Calculate angles from gimbal center
    angle_x = norm_x * (camera_fov_h / 2) * math.pi / 180
    angle_y = norm_y * (camera_fov_v / 2) * math.pi / 180
    
    # Adjust for gimbal elevation
    elevation_rad = gimbal_elevation * math.pi / 180
    
    # Calculate ground distance (simplified - assumes flat earth)
    if elevation_rad >= 0:
        # Camera pointing at or above horizon - no ground intersection
        return platform_lat, platform_lon
    
    ground_distance = altitude / abs(math.tan(elevation_rad + angle_y))
    
    # Calculate bearing
    azimuth_rad = gimbal_azimuth * math.pi / 180
    bearing = azimuth_rad + angle_x
    
    # Convert to lat/lon offset (flat earth approximation)
    # 1 degree latitude ≈ 111,320 meters
    # 1 degree longitude ≈ 111,320 * cos(latitude) meters
    meters_per_deg_lat = 111320.0
    meters_per_deg_lon = 111320.0 * math.cos(platform_lat * math.pi / 180)
    
    # Calculate offset
    offset_north = ground_distance * math.cos(bearing)
    offset_east = ground_distance * math.sin(bearing)
    
    # Convert to lat/lon
    target_lat = platform_lat + (offset_north / meters_per_deg_lat)
    target_lon = platform_lon + (offset_east / meters_per_deg_lon)
    
    return target_lat, target_lon


def calculate_gimbal_delta(
    target_pixel_x: float,
    target_pixel_y: float,
    image_width: int,
    image_height: int,
    camera_fov_h: float = 60.0,
    camera_fov_v: float = 45.0
) -> Tuple[float, float]:
    """
    Calculate gimbal delta angles to center target in frame.
    
    Args:
        target_pixel_x, target_pixel_y: Target pixel coordinates
        image_width, image_height: Image dimensions
        camera_fov_h, camera_fov_v: Camera field of view in degrees
    
    Returns:
        (azimuth_delta, elevation_delta) in degrees
    """
    # Calculate offset from center
    center_x = image_width / 2
    center_y = image_height / 2
    
    offset_x = target_pixel_x - center_x
    offset_y = target_pixel_y - center_y
    
    # Normalize to [-1, 1]
    norm_x = offset_x / center_x
    norm_y = offset_y / center_y
    
    # Convert to angles
    azimuth_delta = norm_x * (camera_fov_h / 2)
    elevation_delta = -norm_y * (camera_fov_v / 2)  # Negative because y increases downward
    
    return azimuth_delta, elevation_delta


def calculate_velocity(
    trajectory: list,
    fps: float = 30.0
) -> Optional[Tuple[float, float]]:
    """
    Calculate velocity from trajectory history.
    
    Args:
        trajectory: List of (x, y, timestamp) tuples
        fps: Frame rate for time calculation
    
    Returns:
        (vx, vy) in pixels per second, or None if insufficient data
    """
    if len(trajectory) < 2:
        return None
    
    # Use last N points for velocity estimation
    n_points = min(10, len(trajectory))
    recent = trajectory[-n_points:]
    
    # Linear regression for velocity
    times = [(p[2] - recent[0][2]).total_seconds() for p in recent]
    xs = [p[0] for p in recent]
    ys = [p[1] for p in recent]
    
    if max(times) - min(times) < 0.1:  # Less than 100ms
        return None
    
    # Simple finite difference
    dt = (recent[-1][2] - recent[0][2]).total_seconds()
    if dt == 0:
        return None
    
    vx = (recent[-1][0] - recent[0][0]) / dt
    vy = (recent[-1][1] - recent[0][1]) / dt
    
    return vx, vy


def stabilize_frame_ecc(
    frame: np.ndarray,
    prev_frame: np.ndarray,
    prev_transform: Optional[np.ndarray] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Stabilize frame using ECC (Enhanced Correlation Coefficient) algorithm.
    
    Args:
        frame: Current frame
        prev_frame: Previous frame
        prev_transform: Previous transformation matrix
    
    Returns:
        (stabilized_frame, transform_matrix)
    """
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    
    # Define motion model (affine)
    warp_mode = cv2.MOTION_AFFINE
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    
    if prev_transform is not None:
        warp_matrix = prev_transform.copy()
    
    # Define termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 50, 0.001)
    
    try:
        # Find transformation
        _, warp_matrix = cv2.findTransformECC(
            prev_gray, gray, warp_matrix, warp_mode, criteria, None, 5
        )
        
        # Apply transformation
        stabilized = cv2.warpAffine(
            frame, warp_matrix, (frame.shape[1], frame.shape[0]),
            flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP
        )
        
        return stabilized, warp_matrix
    except cv2.error:
        # If ECC fails, return original frame
        return frame, warp_matrix


def adaptive_resize(
    frame: np.ndarray,
    altitude: float,
    base_size: int = 640,
    min_altitude: float = 50.0,
    max_altitude: float = 500.0
) -> np.ndarray:
    """
    Adaptively resize frame based on altitude.
    Higher altitude = smaller objects = larger processing size.
    
    Args:
        frame: Input frame
        altitude: Current altitude in meters
        base_size: Base processing size
        min_altitude, max_altitude: Altitude range for scaling
    
    Returns:
        Resized frame
    """
    # Clamp altitude
    altitude = max(min_altitude, min(max_altitude, altitude))
    
    # Scale factor: higher altitude = larger size
    scale = 1.0 + (altitude - min_altitude) / (max_altitude - min_altitude) * 0.5
    target_size = int(base_size * scale)
    
    # Resize maintaining aspect ratio
    h, w = frame.shape[:2]
    if w > h:
        new_w = target_size
        new_h = int(h * target_size / w)
    else:
        new_h = target_size
        new_w = int(w * target_size / h)
    
    resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    return resized


def iou(box1: Tuple[float, float, float, float], 
        box2: Tuple[float, float, float, float]) -> float:
    """
    Calculate Intersection over Union of two boxes.
    
    Args:
        box1, box2: Boxes in (x1, y1, x2, y2) format
    
    Returns:
        IoU value [0, 1]
    """
    x1_1, y1_1, x2_1, y2_1 = box1
    x1_2, y1_2, x2_2, y2_2 = box2
    
    # Intersection
    x1_i = max(x1_1, x1_2)
    y1_i = max(y1_1, y1_2)
    x2_i = min(x2_1, x2_2)
    y2_i = min(y2_1, y2_2)
    
    if x2_i < x1_i or y2_i < y1_i:
        return 0.0
    
    intersection = (x2_i - x1_i) * (y2_i - y1_i)
    
    # Union
    area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
    union = area1 + area2 - intersection
    
    return intersection / union if union > 0 else 0.0


def timestamp_sync(
    frame_timestamp: datetime,
    telemetry_data: list,
    tolerance_ms: float = 100.0
) -> Optional[dict]:
    """
    Find closest telemetry data to frame timestamp.
    
    Args:
        frame_timestamp: Frame timestamp
        telemetry_data: List of telemetry dicts with 'timestamp' key
        tolerance_ms: Maximum time difference in milliseconds
    
    Returns:
        Closest telemetry dict or None
    """
    if not telemetry_data:
        return None
    
    # Make frame_timestamp timezone-aware if it isn't
    if frame_timestamp.tzinfo is None:
        from datetime import timezone
        frame_timestamp = frame_timestamp.replace(tzinfo=timezone.utc)
    
    min_diff = float('inf')
    closest = None
    
    for telem in telemetry_data:
        telem_ts = telem['timestamp']
        # Make telemetry timestamp timezone-aware if needed
        if telem_ts.tzinfo is None:
            from datetime import timezone
            telem_ts = telem_ts.replace(tzinfo=timezone.utc)
        
        diff = abs((telem_ts - frame_timestamp).total_seconds() * 1000)
        if diff < min_diff:
            min_diff = diff
            closest = telem
    
    return closest if min_diff <= tolerance_ms else None
