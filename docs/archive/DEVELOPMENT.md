# Daemon Vision - Development Guide

## Architecture Deep Dive

### Module 1: Sensor Data Ingestion (`src/modules/sensor_ingestion.py`)

Handles video stream input and telemetry synchronization.

Key features:
- RTSP stream support (production) and local video files (development)
- Frame preprocessing: undistortion, ECC stabilization, adaptive resize
- Timestamp synchronization between video frames and telemetry data
- Simulated telemetry generation for testing without real sensor data

Performance considerations:
- Frame buffer to handle burst processing
- Async I/O for non-blocking frame capture
- Adaptive resize based on altitude (higher altitude = larger processing size for small objects)

### Module 2: Object Detection (`src/modules/detection.py`)

YOLOv8-based real-time object detection.

Key features:
- Pre-trained YOLOv8 models (n/s/m/l/x variants)
- GPU acceleration with CUDA + FP16 for 2x speedup
- Configurable confidence and IoU thresholds
- Target class filtering (person, vehicle, aircraft)

Performance optimizations:
- Model warmup on initialization
- Batch processing support (future enhancement)
- TensorRT export for production (future enhancement)

Target: 15+ FPS on RTX 3060 with YOLOv8n

### Module 3: Multi-Target Tracking (`src/modules/tracking.py`)

ByteTrack implementation for persistent target tracking.

Key features:
- Kalman filter for motion prediction
- Two-stage association (high confidence + low confidence)
- Occlusion handling through prediction
- Trajectory history (30 frames default)
- Velocity estimation from trajectory

Why ByteTrack over StrongSORT:
- 30-60ms lower latency (no ReID model)
- Better occlusion handling via BYTE association
- Simpler hyperparameter tuning
- Sufficient for aerial scenarios where appearance changes are gradual

Metrics:
- ID Switch Rate: <0.2% target (1 switch per 500 frames)
- Track persistence: 98%+ through 3s occlusion

### Module 4: Target Locking (`src/modules/locking.py`)

Manages target locks and priority scoring.

Key features:
- Lock persistence through occlusion (3s default)
- Priority scoring: distance (40%) + velocity (30%) + class (30%)
- Gimbal pointing command generation
- Ground coordinate projection (flat-earth approximation)

Lock persistence strategy:
- Maintain lock for N frames after target disappears
- Use Kalman prediction to estimate position during occlusion
- Auto-unlock if occlusion exceeds tolerance

### Module 5: Integration API (`src/modules/api.py`)

FastAPI REST + WebSocket interface.

Endpoints:
- `GET /tracks` - List all active tracks
- `POST /lock/{track_id}` - Lock onto target
- `DELETE /lock` - Release lock
- `GET /track/{track_id}/trajectory` - Get trajectory + prediction slot
- `WS /stream` - Real-time track updates

WebSocket protocol:
```json
{
  "type": "track_update",
  "tracks": [...],
  "timestamp": "2026-03-26T10:30:45.123Z"
}
```

## Performance Tuning

### GPU Optimization

1. Enable FP16 (half precision):
```yaml
detection:
  half_precision: true
```

2. Adjust batch size (future):
```python
# In detection.py
results = self.model.predict(frames, batch=4)
```

3. TensorRT export (production):
```python
model.export(format="engine", half=True)
```

### Latency Budget

Target: <100ms end-to-end (frame in → API response)

Breakdown:
- Frame preprocessing: 5-10ms
- Detection (YOLOv8n): 25-35ms
- Tracking (ByteTrack): 5-10ms
- API serialization: 1-2ms
- Network overhead: 5-10ms

Total: ~60-70ms typical

### Memory Optimization

Current usage (RTX 3060):
- GPU: 2.1GB (model + inference)
- RAM: 450MB (frame buffers + queues)

Reduce memory:
- Smaller model (yolov8n → yolov8n6)
- Reduce frame buffer size
- Lower trajectory history length

## Testing Strategy

### Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific module
pytest tests/test_detection.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

### Integration Tests

```bash
# Full pipeline test
python main.py --video data/sample.mp4 --log-level DEBUG
```

### Benchmark Tests

```bash
# Detection only
python benchmark.py --video data/sample.mp4 --module detection --duration 60

# Tracking only
python benchmark.py --video data/sample.mp4 --module tracking --duration 60

# End-to-end
python benchmark.py --video data/sample.mp4 --module e2e --duration 60
```

## Deployment

### Docker Production Build

```dockerfile
# Use smaller base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Multi-stage build to reduce size
FROM builder AS runtime
COPY --from=builder /app /app
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: daemon-vision
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: daemon-vision
        image: daemon-vision:latest
        resources:
          limits:
            nvidia.com/gpu: 1
```

### Redis Multi-Node Setup

Enable Redis in `docker-compose.yml`:
```yaml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

Update `config.yaml`:
```yaml
queue:
  backend: "redis"
  redis_url: "redis://redis:6379"
```

## Extending the System

### Adding New Target Classes

1. Update `src/core/models.py`:
```python
class TargetClass(str, Enum):
    PERSON = "person"
    CAR = "car"
    DRONE = "drone"  # New class
```

2. Update `config.yaml`:
```yaml
detection:
  target_classes: ["person", "car", "drone"]
```

### Custom Tracking Algorithm

Implement in `src/modules/tracking.py`:
```python
class CustomTracker:
    def update(self, detections, frame_data):
        # Your tracking logic
        return tracks
```

### AI Prediction Integration

1. Subscribe to WebSocket:
```python
import websockets

async with websockets.connect("ws://localhost:8000/stream") as ws:
    async for message in ws:
        data = json.loads(message)
        tracks = data["tracks"]
        # Predict next position
```

2. Add prediction endpoint:
```python
@app.post("/track/{track_id}/prediction")
async def set_prediction(track_id: int, prediction: TrajectoryPoint):
    # Store prediction
    pass
```

## Troubleshooting

### Low FPS

1. Check GPU utilization:
```bash
nvidia-smi -l 1
```

2. Enable profiling:
```python
import cProfile
cProfile.run('asyncio.run(pipeline.run())')
```

3. Reduce model size or image resolution

### High ID Switch Rate

1. Increase IoU threshold:
```yaml
tracking:
  match_thresh: 0.9  # Higher = stricter matching
```

2. Increase track buffer:
```yaml
tracking:
  track_buffer: 120  # Keep tracks longer
```

### Memory Leaks

1. Monitor memory:
```bash
watch -n 1 'nvidia-smi; free -h'
```

2. Check for circular references:
```python
import gc
gc.collect()
print(gc.garbage)
```

## Code Style

Follow PEP 8 with Black formatter:
```bash
black src/ tests/ --line-length 100
ruff check src/ tests/
```

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## License

Confidential - PT. Daemon Blockint Technologies
