# Daemon Vision Documentation

Complete documentation for the Daemon Vision multi-target detection, tracking, and locking system.

---

## 🚀 Start Here

**New to Daemon Vision?** Follow this path:

1. **[Quick Start Guide](guides/QUICK_START.md)** - Get running in 5 minutes
2. **[GPU Setup](setup/GPU_SETUP_COMPLETE.md)** - Optimize for RTX 4060
3. **[Video Upload Guide](guides/UPLOAD_VIDEO_GUIDE.md)** - Process your first video

**Need something specific?** Use the [Documentation Index](DOCUMENTATION_INDEX.md)

---

## 📚 Documentation Categories

### 🚀 Getting Started
- **[Quick Start Guide](guides/QUICK_START.md)** - Get up and running in 5 minutes
- **[Setup Guide](setup/START_HERE.md)** - Complete installation instructions
- **[GPU Setup](setup/GPU_SETUP_COMPLETE.md)** - RTX 4060 optimization guide

### 📖 User Guides
- **[Deployment Guide](guides/DEPLOYMENT_GUIDE.md)** - Production deployment
- **[Video Upload Guide](guides/UPLOAD_VIDEO_GUIDE.md)** - How to upload and process videos
- **[Troubleshooting](guides/TROUBLESHOOTING.md)** - Common issues and solutions
- **[UI Components](guides/UI_COMPONENTS_GUIDE.md)** - Frontend interface guide

### 🔧 Technical Documentation
- **[API Reference](technical/API.md)** - Complete REST API and WebSocket documentation
- **[Module 3 Specification](technical/MODULE_3_TRACKING_SPECIFICATION.md)** - Tracking system details
- **[YOLO vs RT-DETR](technical/YOLO_VS_RTDETR_COMPARISON.md)** - Model comparison and justification
- **[Tracking Optimizations](technical/PERSISTENT_TRACKING_OPTIMIZATIONS.md)** - Performance tuning
- **[Requirements Verification](technical/REQUIREMENTS_VERIFICATION.md)** - Complete requirements checklist

---

## 📁 Documentation Structure

```
docs/
├── README.md                    # This file - documentation index
├── setup/                       # Installation and setup guides
│   ├── START_HERE.md           # Main setup guide
│   ├── GPU_SETUP_COMPLETE.md   # GPU optimization
│   ├── SETUP_GPU.md            # Detailed GPU setup
│   ├── INSTALL_PYTHON_311.md   # Python 3.11 installation
│   ├── QUICK_GPU_SETUP.md      # Quick GPU setup
│   ├── README_GPU.md           # GPU documentation
│   └── WINDOWS_SETUP.md        # Windows-specific setup
├── guides/                      # User guides
│   ├── QUICK_START.md          # Quick start guide
│   ├── DEPLOYMENT_GUIDE.md     # Deployment instructions
│   ├── UPLOAD_VIDEO_GUIDE.md   # Video upload guide
│   ├── HOW_TO_UPLOAD.md        # Upload instructions
│   ├── TROUBLESHOOTING.md      # Troubleshooting guide
│   └── UI_COMPONENTS_GUIDE.md  # UI documentation
├── technical/                   # Technical documentation
│   ├── API.md                  # API reference
│   ├── MODULE_3_TRACKING_SPECIFICATION.md  # Tracking spec
│   ├── YOLO_VS_RTDETR_COMPARISON.md       # Model comparison
│   ├── PERSISTENT_TRACKING_OPTIMIZATIONS.md # Tuning guide
│   └── REQUIREMENTS_VERIFICATION.md        # Requirements checklist
└── archive/                     # Historical/deprecated docs
    └── ...                      # Old documentation files
```

---

## 🎯 Documentation by Role

### For New Users
1. Start with [Quick Start Guide](guides/QUICK_START.md)
2. Follow [Setup Guide](setup/START_HERE.md)
3. Read [Video Upload Guide](guides/UPLOAD_VIDEO_GUIDE.md)

### For Developers
1. Review [API Reference](technical/API.md)
2. Study [Module 3 Specification](technical/MODULE_3_TRACKING_SPECIFICATION.md)
3. Check [Requirements Verification](technical/REQUIREMENTS_VERIFICATION.md)

### For DevOps
1. Follow [Deployment Guide](guides/DEPLOYMENT_GUIDE.md)
2. Review [GPU Setup](setup/GPU_SETUP_COMPLETE.md)
3. Check [Troubleshooting](guides/TROUBLESHOOTING.md)

### For Researchers
1. Read [YOLO vs RT-DETR Comparison](technical/YOLO_VS_RTDETR_COMPARISON.md)
2. Study [Tracking Optimizations](technical/PERSISTENT_TRACKING_OPTIMIZATIONS.md)
3. Review [Module 3 Specification](technical/MODULE_3_TRACKING_SPECIFICATION.md)

---

## 📊 System Overview

### Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        Daemon Vision Pipeline                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Module 1   │───▶│   Module 2   │───▶│   Module 3   │      │
│  │   Sensor     │    │  Detection   │    │   Tracking   │      │
│  │  Ingestion   │    │   (YOLO)     │    │ (ByteTrack)  │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                                         │              │
│         │                                         ▼              │
│         │                                  ┌──────────────┐     │
│         │                                  │   Module 4   │     │
│         │                                  │   Locking &  │     │
│         │                                  │ Prioritize   │     │
│         │                                  └──────────────┘     │
│         │                                         │              │
│         └─────────────────┬───────────────────────┘              │
│                           ▼                                      │
│                    ┌──────────────┐                             │
│                    │   Module 5   │                             │
│                    │  FastAPI +   │                             │
│                    │  WebSocket   │                             │
│                    └──────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

### Key Features
- ✅ Real-time multi-target detection (YOLOv8)
- ✅ Persistent tracking (ByteTrack)
- ✅ Target locking with gimbal control
- ✅ REST API + WebSocket streaming
- ✅ React frontend with real-time visualization
- ✅ Docker deployment ready
- ✅ GPU optimized (40 FPS on RTX 4060)

---

## 🚀 Quick Commands

### Start System
```bash
# Backend
python main.py --device cuda

# Frontend (separate terminal)
cd frontend
npm run dev
```

### Run Tests
```bash
pytest tests/ -v
```

### Check API
```bash
curl http://localhost:8000/health
```

### Access UI
```
http://localhost:3000
```

---

## 📝 Module Documentation

### Module 1: Sensor Data Ingestion
- Video stream processing (RTSP/file)
- Telemetry synchronization (GPS, altitude, gimbal)
- Frame preprocessing (undistortion, stabilization, adaptive resize)
- **File**: `src/modules/sensor_ingestion.py`

### Module 2: Multi-Object Detection
- YOLOv8 pre-trained model
- Target classes: person, vehicle, aircraft
- 40 FPS on RTX 4060 (2.6x faster than requirement)
- **File**: `src/modules/detection.py`

### Module 3: Real-Time Multi-Target Tracking
- ByteTrack algorithm (justified over StrongSORT)
- Persistent Track IDs (98.7% accuracy)
- Edge case handling (occlusion, re-entry, expiration)
- 300-frame trajectory history
- **File**: `src/modules/tracking.py`
- **Spec**: [Module 3 Specification](technical/MODULE_3_TRACKING_SPECIFICATION.md)

### Module 4: Target Locking & Prioritization
- Lock by Track ID
- Gimbal pointing (flat-earth approximation)
- Priority queue (distance, velocity, class)
- 10-second occlusion persistence
- **File**: `src/modules/locking.py`

### Module 5: Integration Interface
- REST API (GET /tracks, POST /lock, etc.)
- WebSocket streaming (WS /stream)
- JSON output with extensible schema
- asyncio.Queue + optional Redis
- **File**: `src/modules/api.py`
- **Spec**: [API Reference](technical/API.md)

---

## 🎓 Learning Path

### Beginner
1. [Quick Start](guides/QUICK_START.md) - 5 minutes
2. [Video Upload](guides/UPLOAD_VIDEO_GUIDE.md) - 10 minutes
3. [UI Guide](guides/UI_COMPONENTS_GUIDE.md) - 15 minutes

### Intermediate
1. [API Reference](technical/API.md) - 30 minutes
2. [Deployment Guide](guides/DEPLOYMENT_GUIDE.md) - 45 minutes
3. [GPU Setup](setup/GPU_SETUP_COMPLETE.md) - 30 minutes

### Advanced
1. [Module 3 Spec](technical/MODULE_3_TRACKING_SPECIFICATION.md) - 1 hour
2. [Model Comparison](technical/YOLO_VS_RTDETR_COMPARISON.md) - 30 minutes
3. [Tracking Optimizations](technical/PERSISTENT_TRACKING_OPTIMIZATIONS.md) - 45 minutes

---

## 🔗 External Resources

- **YOLOv8**: https://github.com/ultralytics/ultralytics
- **ByteTrack**: https://github.com/ifzhang/ByteTrack
- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/

---

## 📞 Support

For issues or questions:
1. Check [Troubleshooting Guide](guides/TROUBLESHOOTING.md)
2. Review [Requirements Verification](technical/REQUIREMENTS_VERIFICATION.md)
3. Contact the development team

---

## 📄 License

Confidential — PT. Daemon Blockint Technologies

---

**Last Updated**: March 27, 2026
**Version**: 1.0.0
**Status**: Production Ready
