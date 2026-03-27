# Data Directory

This directory contains video files and telemetry data for Daemon Vision.

## Required Files

### Video File
Place your aerial surveillance video here:
- Format: MP4, AVI, MOV, or RTSP stream URL
- Resolution: Any (will be resized to 640x640)
- Frame rate: 30 FPS recommended
- Example: `sample.mp4`

### Telemetry File (Optional)
JSON file with platform telemetry data:
- Format: JSON array of telemetry entries
- Example: `telemetry.json`

## Telemetry Format

```json
[
  {
    "timestamp": "2026-03-26T10:30:00.000Z",
    "gps": {
      "lat": -6.2088,
      "lon": 106.8456
    },
    "altitude": 150.0,
    "gimbal_azimuth": 0.0,
    "gimbal_elevation": -45.0,
    "heading": 90.0
  }
]
```

Fields:
- `timestamp`: ISO 8601 format
- `gps.lat`: Latitude in degrees
- `gps.lon`: Longitude in degrees
- `altitude`: Altitude above ground in meters
- `gimbal_azimuth`: Gimbal azimuth in degrees (0 = North, clockwise)
- `gimbal_elevation`: Gimbal elevation in degrees (negative = down)
- `heading`: Platform heading in degrees

## Sample Data

If no telemetry file is provided, the system will generate simulated telemetry data for testing.

## Getting Sample Videos

For testing, you can use:
1. Drone footage from YouTube (use youtube-dl)
2. Public datasets: VisDrone, UAVDT
3. Your own aerial footage

Example download:
```bash
# Install youtube-dl
pip install youtube-dl

# Download sample drone video
youtube-dl -f mp4 "https://www.youtube.com/watch?v=DRONE_VIDEO_ID" -o data/sample.mp4
```

## File Size Recommendations

- Video: <500MB for quick testing
- Duration: 30-60 seconds sufficient for demo
- Resolution: 1080p or higher (will be downscaled)
