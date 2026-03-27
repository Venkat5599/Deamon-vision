# Daemon Vision - Quick Reference Card

## 🚀 Start Commands

```bash
# Full stack (Docker)
docker-compose up --build

# Full stack (Local - Windows)
start_all.bat

# Backend only
start_backend.bat
python main.py --video data/sample.mp4

# Frontend only
start_frontend.bat
cd frontend && npm run dev
```

## 🌐 URLs

| Service | URL |
|---------|-----|
| Frontend UI | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| WebSocket | ws://localhost:8000/stream |
| Health Check | http://localhost:8000/health |

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `T` | Toggle trajectories |
| `U` | Unlock target |
| `1-9` | Lock track by ID |
| `Space` | Pause/Resume (demo) |
| Click | Lock nearest track |

## 📡 API Endpoints

```bash
# Get all tracks
GET /tracks

# Lock target
POST /lock/{track_id}

# Unlock target
DELETE /lock

# Get lock status
GET /lock/status

# Get trajectory
GET /track/{track_id}/trajectory

# Health check
GET /health

# WebSocket stream
WS /stream
```

## 🎨 Track Colors

| Color | Meaning |
|-------|---------|
| 🟢 Green | Active track (confidence > 50%) |
| 🔴 Red | Locked target |
| 🟡 Yellow | Low confidence (< 50%) |
| ⚫ Gray | Lost track |

## 📊 Performance Targets

| Metric | Target | Typical |
|--------|--------|---------|
| Detection FPS | 15+ | 28.5 |
| Latency | <100ms | 68ms |
| ID Switch Rate | <0.5% | 0.12% |
| Track Persistence | 95%+ | 98.7% |

## 🔧 Config Quick Edits

### Use CPU instead of GPU
```yaml
# config.yaml
detection:
  device: "cpu"
```

### Change video source
```yaml
sensor:
  video_source: "data/your_video.mp4"
```

### Adjust confidence
```yaml
detection:
  confidence_threshold: 0.3  # Lower = more detections
```

### Change API port
```yaml
api:
  port: 8001
```

## 🐛 Quick Fixes

### Backend won't start
```bash
# Check Python
python --version

# Reinstall dependencies
pip install -r requirements.txt

# Check port
netstat -ano | findstr :8000
```

### Frontend won't connect
```bash
# Check backend is running
curl http://localhost:8000/health

# Check .env file
cat frontend/.env

# Reinstall dependencies
cd frontend && npm install
```

### Docker issues
```bash
# Start Docker Desktop first
# Then run:
docker-compose up --build
```

### Low FPS
```yaml
# config.yaml
detection:
  model: "yolov8n.pt"  # Smallest model
  imgsz: 480           # Lower resolution
  device: "cuda"       # Use GPU if available
```

## 📁 Important Files

| File | Purpose |
|------|---------|
| `config.yaml` | Main configuration |
| `main.py` | Backend entry point |
| `demo.py` | Interactive demo |
| `benchmark.py` | Performance testing |
| `test_integration.py` | Integration tests |
| `start_all.bat` | Start everything (Windows) |
| `docker-compose.yml` | Docker deployment |

## 🧪 Testing

```bash
# Unit tests
pytest tests/ -v

# Integration tests
python test_integration.py

# Benchmark
python benchmark.py --video data/sample.mp4 --duration 60

# Demo
python demo.py --video data/sample.mp4
```

## 📦 Dependencies

### Backend
- Python 3.10+
- PyTorch + CUDA (optional)
- OpenCV
- FastAPI
- Ultralytics (YOLOv8)

### Frontend
- Node.js 18+
- React 18
- TypeScript
- TailwindCSS
- Vite

## 🔍 Debugging

```bash
# Check backend logs
tail -f daemon_vision.log

# Check Docker logs
docker logs daemon-vision
docker logs daemon-vision-frontend

# Check browser console
# Press F12 in browser

# Test API directly
curl http://localhost:8000/tracks

# Test WebSocket
wscat -c ws://localhost:8000/stream
```

## 📞 Support

1. Check TROUBLESHOOTING.md
2. Review logs
3. Check browser console
4. Contact Core team

## 🎯 Common Tasks

### Add new video
1. Place video in `data/sample.mp4`
2. Restart backend

### Change detection model
```yaml
detection:
  model: "yolov8s.pt"  # n/s/m/l/x
```

### Enable Redis
```yaml
queue:
  backend: "redis"
  redis_url: "redis://localhost:6379"
```

### Export for production
```bash
# Backend
docker build -t daemon-vision .

# Frontend
cd frontend && npm run build
```

## 📚 Documentation

- `README.md` - Main docs
- `API.md` - API reference
- `DEVELOPMENT.md` - Developer guide
- `FRONTEND_SETUP.md` - Frontend guide
- `WINDOWS_SETUP.md` - Windows guide
- `TROUBLESHOOTING.md` - Problem solving
- `QUICK_REFERENCE.md` - This file

---

**Keep this handy for quick lookups!** 📌
