# Daemon Vision - Project Structure

## 📁 Directory Organization

```
daemon-vision/
├── 📄 README.md                    # Main project documentation
├── 📄 config.yaml                  # System configuration
├── 📄 requirements.txt             # Python dependencies
├── 📄 main.py                      # Application entry point
├── 📄 Dockerfile                   # Container definition
├── 📄 docker-compose.yml           # Multi-container orchestration
│
├── 📂 docs/                        # 📚 Documentation
│   ├── README.md                   # Documentation index
│   ├── setup/                      # Installation guides
│   │   ├── START_HERE.md          # Main setup guide
│   │   ├── GPU_SETUP_COMPLETE.md  # GPU optimization
│   │   └── ...
│   ├── guides/                     # User guides
│   │   ├── QUICK_START.md         # Quick start
│   │   ├── DEPLOYMENT_GUIDE.md    # Deployment
│   │   └── ...
│   ├── technical/                  # Technical docs
│   │   ├── API.md                 # API reference
│   │   ├── MODULE_3_TRACKING_SPECIFICATION.md
│   │   └── ...
│   └── archive/                    # Historical docs
│
├── 📂 src/                         # 🔧 Source Code
│   ├── __init__.py
│   ├── pipeline.py                 # Main pipeline orchestrator
│   ├── modules/                    # Core modules
│   │   ├── sensor_ingestion.py    # Module 1: Sensor data
│   │   ├── detection.py           # Module 2: Object detection
│   │   ├── tracking.py            # Module 3: Multi-target tracking
│   │   ├── locking.py             # Module 4: Target locking
│   │   └── api.py                 # Module 5: REST API + WebSocket
│   └── core/                       # Shared utilities
│       ├── models.py               # Data models (Pydantic)
│       ├── utils.py                # Helper functions
│       └── queue_manager.py        # Queue management
│
├── 📂 tests/                       # 🧪 Test Suite
│   ├── test_detection.py          # Detection tests
│   ├── test_tracking.py           # Tracking tests
│   ├── test_tracking_edge_cases.py # Edge case tests
│   └── test_api.py                # API tests
│
├── 📂 frontend/                    # 🎨 Web Interface
│   ├── package.json               # Node dependencies
│   ├── vite.config.ts             # Vite configuration
│   ├── src/
│   │   ├── App.tsx                # Main application
│   │   ├── components/            # React components
│   │   │   ├── Header.tsx
│   │   │   ├── VideoFeed.tsx
│   │   │   ├── TrackList.tsx
│   │   │   └── ...
│   │   ├── hooks/                 # Custom hooks
│   │   │   └── useWebSocket.ts
│   │   └── utils/                 # Utilities
│   │       ├── api.ts
│   │       └── canvas.ts
│   └── dist/                      # Build output
│
├── 📂 data/                        # 📊 Data Files
│   ├── README.md                  # Data documentation
│   ├── telemetry.json             # Sample telemetry
│   └── uploaded_video.mp4         # Test video
│
├── 📂 scripts/                     # 🛠️ Utility Scripts
│   ├── setup_gpu.bat              # GPU setup (Windows)
│   ├── setup_gpu.ps1              # GPU setup (PowerShell)
│   ├── start_all.bat              # Start all services
│   ├── benchmark.py               # Performance benchmark
│   ├── demo.py                    # Demo script
│   └── check_status.py            # System status check
│
└── 📂 venv311/                     # 🐍 Python Virtual Environment
    └── ...                         # (Python 3.11 with CUDA)
```

---

## 🎯 Key Files

### Configuration
- `config.yaml` - System configuration (detection, tracking, API settings)
- `.env.production` - Production environment variables
- `docker-compose.yml` - Container orchestration

### Entry Points
- `main.py` - Main application (backend)
- `frontend/src/main.tsx` - Frontend application
- `demo.py` - Standalone demo script

### Core Modules
- `src/modules/sensor_ingestion.py` - Video + telemetry processing
- `src/modules/detection.py` - YOLOv8 object detection
- `src/modules/tracking.py` - ByteTrack multi-target tracking
- `src/modules/locking.py` - Target locking + prioritization
- `src/modules/api.py` - FastAPI REST + WebSocket

### Documentation
- `README.md` - Main project README
- `docs/README.md` - Documentation index
- `docs/technical/API.md` - API reference
- `docs/technical/MODULE_3_TRACKING_SPECIFICATION.md` - Tracking spec

---

## 📦 Dependencies

### Backend (Python)
```
ultralytics      # YOLOv8
fastapi          # REST API
opencv-python    # Computer vision
numpy            # Numerical computing
filterpy         # Kalman filter
lap              # Linear assignment
```

### Frontend (Node.js)
```
react            # UI framework
typescript       # Type safety
vite             # Build tool
tailwindcss      # Styling
lucide-react     # Icons
```

---

## 🚀 Quick Navigation

### For Development
- Source code: `src/`
- Tests: `tests/`
- Configuration: `config.yaml`

### For Documentation
- All docs: `docs/`
- API reference: `docs/technical/API.md`
- Setup guide: `docs/setup/START_HERE.md`

### For Deployment
- Docker: `Dockerfile`, `docker-compose.yml`
- Scripts: `setup_gpu.bat`, `start_all.bat`
- Deployment guide: `docs/guides/DEPLOYMENT_GUIDE.md`

---

## 🔧 Development Workflow

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Setup GPU (Windows)
.\setup_gpu.bat
```

### 2. Development
```bash
# Run backend
python main.py --device cuda

# Run frontend (separate terminal)
cd frontend
npm run dev
```

### 3. Testing
```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_tracking_edge_cases.py -v
```

### 4. Deployment
```bash
# Build containers
docker-compose build

# Start services
docker-compose up -d
```

---

## 📊 Module Dependencies

```
main.py
  └── src/pipeline.py
      ├── src/modules/sensor_ingestion.py
      │   └── src/core/utils.py
      ├── src/modules/detection.py
      │   └── src/core/models.py
      ├── src/modules/tracking.py
      │   ├── src/core/models.py
      │   └── src/core/utils.py
      ├── src/modules/locking.py
      │   ├── src/core/models.py
      │   └── src/core/utils.py
      └── src/modules/api.py
          ├── src/core/models.py
          └── src/core/queue_manager.py
```

---

## 🎨 Frontend Structure

```
frontend/
├── src/
│   ├── App.tsx                    # Main app component
│   ├── main.tsx                   # Entry point
│   ├── index.css                  # Global styles
│   ├── components/                # React components
│   │   ├── Header.tsx            # Top navigation
│   │   ├── VideoFeed.tsx         # Video display + canvas
│   │   ├── TrackList.tsx         # Track list sidebar
│   │   ├── TrackCard.tsx         # Individual track card
│   │   ├── MetricsDashboard.tsx  # Metrics display
│   │   └── ui/                   # shadcn/ui components
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       └── badge.tsx
│   ├── hooks/                     # Custom React hooks
│   │   └── useWebSocket.ts       # WebSocket connection
│   ├── utils/                     # Utilities
│   │   ├── api.ts                # API client
│   │   └── canvas.ts             # Canvas drawing
│   └── types/                     # TypeScript types
│       └── index.ts
└── dist/                          # Build output
```

---

## 🗂️ Data Flow

```
Video File → Sensor Ingestion → Detection → Tracking → Locking → API
                ↓                   ↓          ↓         ↓        ↓
           Telemetry.json      Detections   Tracks   Lock    WebSocket
                                                              ↓
                                                         Frontend UI
```

---

## 📝 File Naming Conventions

- **Python modules**: `snake_case.py`
- **TypeScript files**: `PascalCase.tsx` (components), `camelCase.ts` (utilities)
- **Documentation**: `UPPER_CASE.md`
- **Configuration**: `lowercase.yaml`, `lowercase.json`
- **Scripts**: `snake_case.py`, `kebab-case.bat`

---

## 🔍 Finding Things

### "Where is the detection code?"
→ `src/modules/detection.py`

### "How do I configure tracking?"
→ `config.yaml` (tracking section)

### "Where are the API endpoints?"
→ `src/modules/api.py` + `docs/technical/API.md`

### "How do I setup GPU?"
→ `docs/setup/GPU_SETUP_COMPLETE.md`

### "Where are the tests?"
→ `tests/` directory

### "How do I deploy?"
→ `docs/guides/DEPLOYMENT_GUIDE.md`

---

**Last Updated**: March 27, 2026
**Version**: 1.0.0
