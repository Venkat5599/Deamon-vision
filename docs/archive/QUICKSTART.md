# Daemon Vision - Quick Start Guide

## 5-Minute Setup

### Prerequisites
- Python 3.10+
- NVIDIA GPU with CUDA 11.8+ (or CPU for testing)
- Docker (optional)

### Option 1: Docker (Fastest)

```bash
# Clone repository
git clone <repo-url>
cd daemon-vision

# Place your video in data/ folder
cp /path/to/your/video.mp4 data/sample.mp4

# Build and run
docker-compose up --build

# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Option 2: Local Setup

```bash
# Clone repository
git clone <repo-url>
cd daemon-vision

# Run setup script
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Run with sample video
python main.py --video data/sample.mp4
```

## First Run

### 1. Test with Demo Script

```bash
# Interactive demo with visualization
python demo.py --video data/sample.mp4

# Controls:
# SPACE - Pause/Resume
# T - Toggle Trajectories
# A - Auto-lock Highest Priority
# 1-9 - Lock Track by ID
# U - Unlock
# Q - Quit
```

### 2. Access API

Open browser to http://localhost:8000/docs for interactive API documentation.

### 3. Test WebSocket

```python
import asyncio
import websockets
import json

async def test_websocket():
    async with websockets.connect("ws://localhost:8000/stream") as ws:
        async for message in ws:
            data = json.loads(message)
            print(f"Received {len(data.get('tracks', []))} tracks")

asyncio.run(test_websocket())
```

## Common Commands

### Run with Custom Config
```bash
python main.py --config my_config.yaml
```

### Run on CPU
```bash
python main.py --video data/sample.mp4 --device cpu
```

### Run Benchmark
```bash
python benchmark.py --video data/sample.mp4 --duration 60
```

### Run Tests
```bash
pytest tests/ -v
```

## API Quick Reference

### Get All Tracks
```bash
curl http://localhost:8000/tracks
```

### Lock Target
```bash
curl -X POST http://localhost:8000/lock/1
```

### Get Trajectory
```bash
curl http://localhost:8000/track/1/trajectory
```

### Unlock
```bash
curl -X DELETE http://localhost:8000/lock
```

## Configuration Quick Tweaks

Edit `config.yaml`:

### Increase FPS (lower accuracy)
```yaml
detection:
  model: "yolov8n.pt"  # Smallest model
  imgsz: 480           # Smaller size
```

### Increase Accuracy (lower FPS)
```yaml
detection:
  model: "yolov8m.pt"  # Medium model
  confidence_threshold: 0.3
```

### Adjust Tracking Sensitivity
```yaml
tracking:
  track_thresh: 0.3    # Lower = more tracks
  match_thresh: 0.9    # Higher = stricter matching
```

## Troubleshooting

### "CUDA out of memory"
```yaml
detection:
  half_precision: true
  imgsz: 480
```

### "Low FPS"
1. Check GPU usage: `nvidia-smi`
2. Use smaller model: `yolov8n.pt`
3. Reduce image size: `imgsz: 480`

### "Too many ID switches"
```yaml
tracking:
  match_thresh: 0.9
  track_buffer: 120
```

### "Can't find video file"
```bash
# Check file exists
ls -la data/

# Use absolute path
python main.py --video /absolute/path/to/video.mp4
```

## Next Steps

1. Read [README.md](README.md) for full documentation
2. Check [API.md](API.md) for API reference
3. See [DEVELOPMENT.md](DEVELOPMENT.md) for advanced topics
4. Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture

## Getting Help

1. Check logs: `tail -f daemon_vision.log`
2. Enable debug logging: `--log-level DEBUG`
3. Run tests: `pytest tests/ -v`
4. Contact Core team

## Sample Output

```
==========================================
Daemon Vision - Multi-Target Detection & Tracking System
PT. Daemon Blockint Technologies
==========================================
2026-03-26 10:30:00 - INFO - Initializing Daemon Vision pipeline...
2026-03-26 10:30:01 - INFO - Video properties: 1920x1080 @ 30.0 FPS, 900 frames
2026-03-26 10:30:02 - INFO - Model loaded on CUDA with FP16: True
2026-03-26 10:30:03 - INFO - Pipeline initialization complete
2026-03-26 10:30:03 - INFO - Starting Daemon Vision pipeline...
2026-03-26 10:30:04 - INFO - Frame 30 | Pipeline FPS: 28.50 | Detection FPS: 29.20 | Active tracks: 5
```

## Quick Performance Check

```bash
# Run 60-second benchmark
python benchmark.py --video data/sample.mp4 --duration 60

# Expected output (RTX 3060):
# Average FPS: 28.5
# Average latency: 68ms
# ID switch rate: 0.12%
```

## Production Checklist

- [ ] Configure authentication
- [ ] Set CORS origins
- [ ] Enable HTTPS
- [ ] Add rate limiting
- [ ] Setup monitoring
- [ ] Configure Redis for multi-node
- [ ] Add persistent storage
- [ ] Setup backup strategy

---

**You're ready to go! 🚀**
