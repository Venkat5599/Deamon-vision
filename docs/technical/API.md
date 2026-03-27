# Daemon Vision API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently no authentication required. Add API keys in production.

---

## REST Endpoints

### Health Check

#### `GET /health`
Check system health and status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-26T10:30:45.123Z",
  "active_tracks": 5,
  "websocket_connections": 2
}
```

---

### List All Tracks

#### `GET /tracks`
Get all currently active tracks.

**Response:**
```json
{
  "tracks": [
    {
      "track_id": 1,
      "class_name": "vehicle",
      "confidence": 0.92,
      "bbox": {
        "x": 100.5,
        "y": 200.3,
        "w": 50.2,
        "h": 60.1
      },
      "ground_coord": {
        "lat": -6.2088,
        "lon": 106.8456,
        "alt": 0.0
      },
      "velocity": {
        "vx": 2.3,
        "vy": -1.1
      },
      "trajectory": [
        {
          "x": 100.0,
          "y": 200.0,
          "timestamp": "2026-03-26T10:30:44.000Z"
        }
      ],
      "last_seen": "2026-03-26T10:30:45.123Z",
      "frames_since_update": 0,
      "is_locked": false
    }
  ],
  "timestamp": "2026-03-26T10:30:45.123Z"
}
```

---

### Lock Target

#### `POST /lock/{track_id}`
Lock onto a specific target by track ID.

**Parameters:**
- `track_id` (path): Track ID to lock

**Response:**
```json
{
  "track_id": 1,
  "locked": true,
  "gimbal_delta": {
    "azimuth": 12.5,
    "elevation": -8.3
  },
  "timestamp": "2026-03-26T10:30:45.123Z"
}
```

**Error Responses:**
- `404`: Track not found
- `500`: Lock manager not initialized

---

### Unlock Target

#### `DELETE /lock`
Release current lock.

**Response:**
```json
{
  "locked": false,
  "timestamp": "2026-03-26T10:30:45.123Z"
}
```

---

### Get Lock Status

#### `GET /lock/status`
Get current lock status.

**Response:**
```json
{
  "locked": true,
  "track_id": 1,
  "lock_timestamp": "2026-03-26T10:30:40.000Z",
  "frames_since_seen": 0,
  "occlusion_tolerance": 90,
  "timestamp": "2026-03-26T10:30:45.123Z"
}
```

---

### Get Track Trajectory

#### `GET /track/{track_id}/trajectory`
Get trajectory history for a specific track.

**Parameters:**
- `track_id` (path): Track ID

**Response:**
```json
{
  "track_id": 1,
  "trajectory": [
    {
      "x": 100.0,
      "y": 200.0,
      "timestamp": "2026-03-26T10:30:44.000Z"
    },
    {
      "x": 102.3,
      "y": 198.9,
      "timestamp": "2026-03-26T10:30:44.033Z"
    }
  ],
  "predicted_position": null,
  "velocity": {
    "vx": 2.3,
    "vy": -1.1
  }
}
```

**Note:** `predicted_position` is reserved for AI prediction module integration.

**Error Responses:**
- `404`: Track not found

---

## WebSocket

### Real-Time Track Stream

#### `WS /stream`
WebSocket endpoint for real-time track updates.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/stream');

ws.onopen = () => {
  console.log('Connected to Daemon Vision');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

**Message Types:**

1. **Connected**
```json
{
  "type": "connected",
  "message": "Connected to Daemon Vision stream",
  "timestamp": "2026-03-26T10:30:45.123Z"
}
```

2. **Track Update**
```json
{
  "type": "track_update",
  "tracks": [
    {
      "track_id": 1,
      "class_name": "vehicle",
      "confidence": 0.92,
      "bbox": {...},
      "velocity": {...},
      "trajectory": [...],
      "last_seen": "2026-03-26T10:30:45.123Z",
      "is_locked": false
    }
  ],
  "timestamp": "2026-03-26T10:30:45.123Z"
}
```

3. **Heartbeat**
```json
{
  "type": "heartbeat",
  "timestamp": "2026-03-26T10:30:45.123Z"
}
```

**Client Heartbeat:**
Send `"ping"` to receive `"pong"` response.

---

## Data Models

### BoundingBox
```typescript
{
  x: number,      // Top-left x coordinate
  y: number,      // Top-left y coordinate
  w: number,      // Width
  h: number       // Height
}
```

### GroundCoordinate
```typescript
{
  lat: number,    // Latitude in degrees
  lon: number,    // Longitude in degrees
  alt: number     // Altitude in meters (0 for ground)
}
```

### Velocity
```typescript
{
  vx: number,     // Velocity in x direction (m/s)
  vy: number      // Velocity in y direction (m/s)
}
```

### TrajectoryPoint
```typescript
{
  x: number,              // X coordinate
  y: number,              // Y coordinate
  timestamp: string       // ISO 8601 timestamp
}
```

### GimbalCommand
```typescript
{
  azimuth: number,        // Azimuth delta in degrees
  elevation: number       // Elevation delta in degrees
}
```

---

## Example Usage

### Python Client

```python
import requests
import json

# Get all tracks
response = requests.get('http://localhost:8000/tracks')
tracks = response.json()['tracks']

# Lock onto first track
if tracks:
    track_id = tracks[0]['track_id']
    response = requests.post(f'http://localhost:8000/lock/{track_id}')
    lock_data = response.json()
    print(f"Locked onto track {track_id}")
    print(f"Gimbal delta: {lock_data['gimbal_delta']}")

# Get trajectory
response = requests.get(f'http://localhost:8000/track/{track_id}/trajectory')
trajectory = response.json()
print(f"Trajectory points: {len(trajectory['trajectory'])}")
```

### JavaScript Client

```javascript
// REST API
async function getTracks() {
  const response = await fetch('http://localhost:8000/tracks');
  const data = await response.json();
  return data.tracks;
}

async function lockTarget(trackId) {
  const response = await fetch(`http://localhost:8000/lock/${trackId}`, {
    method: 'POST'
  });
  return await response.json();
}

// WebSocket
const ws = new WebSocket('ws://localhost:8000/stream');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'track_update') {
    updateUI(data.tracks);
  }
};

function updateUI(tracks) {
  tracks.forEach(track => {
    console.log(`Track ${track.track_id}: ${track.class_name} at (${track.bbox.x}, ${track.bbox.y})`);
  });
}
```

### cURL Examples

```bash
# Get all tracks
curl http://localhost:8000/tracks

# Lock target
curl -X POST http://localhost:8000/lock/1

# Get trajectory
curl http://localhost:8000/track/1/trajectory

# Unlock
curl -X DELETE http://localhost:8000/lock

# Health check
curl http://localhost:8000/health
```

---

## Rate Limits

Currently no rate limits. Recommended for production:
- REST API: 100 requests/minute per client
- WebSocket: 1 connection per client

---

## CORS

CORS is enabled for all origins by default. Configure in `config.yaml`:

```yaml
api:
  cors_origins: ["http://localhost:3000", "https://yourdomain.com"]
```

---

## Interactive Documentation

FastAPI provides automatic interactive documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message"
}
```

HTTP Status Codes:
- `200`: Success
- `404`: Resource not found
- `500`: Internal server error

---

## Future Enhancements

1. **Authentication**: JWT tokens for secure access
2. **Prediction Endpoint**: POST predicted positions from AI module
3. **Batch Operations**: Lock/unlock multiple targets
4. **Historical Data**: Query past tracks and trajectories
5. **Metrics Endpoint**: Performance metrics and statistics
