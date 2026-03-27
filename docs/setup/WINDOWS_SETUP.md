# Daemon Vision - Windows Setup Guide

## 🚀 Quick Start (3 Steps)

### Step 1: Install Prerequisites

1. **Python 3.10+**
   - Download: https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH" during installation
   - Verify: `python --version`

2. **Node.js 18+**
   - Download: https://nodejs.org/
   - Install LTS version
   - Verify: `node --version` and `npm --version`

3. **Git** (optional)
   - Download: https://git-scm.com/download/win
   - Or download project as ZIP

### Step 2: Setup Project

**Double-click**: `start_local.bat`

This will:
- Create Python virtual environment
- Install Python dependencies
- Install Node.js dependencies

### Step 3: Run System

**Double-click**: `start_all.bat`

This will open two windows:
- Backend (Python) - http://localhost:8000
- Frontend (React) - http://localhost:3000

**Open browser**: http://localhost:3000

## 📁 Project Files

```
daemon-vision/
├── start_local.bat      ← Setup (run once)
├── start_all.bat        ← Start everything
├── start_backend.bat    ← Start backend only
├── start_frontend.bat   ← Start frontend only
├── data/
│   └── sample.mp4       ← Put your video here
└── ...
```

## 🎥 Adding Video

1. Get a video file (MP4, AVI, MOV)
2. Rename it to `sample.mp4`
3. Place in `data/` folder
4. Restart backend

**No video?** System will work with simulated data.

## ⚙️ Configuration

Edit `config.yaml` to customize:

```yaml
sensor:
  video_source: "data/sample.mp4"  # Your video
  fps: 30

detection:
  device: "cpu"  # or "cuda" for GPU
  confidence_threshold: 0.5

api:
  port: 8000
```

## 🔧 Troubleshooting

### "Python not found"

**Solution**: Install Python and check "Add to PATH"

Or use: `py` instead of `python`

### "npm not found"

**Solution**: Install Node.js from https://nodejs.org/

### "Port 8000 already in use"

**Solution**: 
```bash
# Find process
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

### Backend won't start

**Solution**:
1. Open Command Prompt as Administrator
2. Run: `start_backend.bat`
3. Check for error messages

### Frontend shows "Cannot connect"

**Solution**:
1. Ensure backend is running first
2. Check http://localhost:8000/health
3. Restart frontend

## 🎮 Using the Interface

### Main Screen

- **Left**: Video feed with track overlays
- **Right**: Track list with details
- **Bottom**: Performance metrics

### Controls

- **Click track card** → Lock/unlock target
- **Click on video** → Lock nearest track
- **Press T** → Toggle trajectories
- **Press U** → Unlock current target
- **Press 1-9** → Lock track by ID

### Track Colors

- 🟢 **Green**: Active track (good confidence)
- 🔴 **Red**: Locked target
- 🟡 **Yellow**: Low confidence

## 📊 Performance Tips

### For Better FPS

1. **Use GPU** (if available):
   ```yaml
   detection:
     device: "cuda"
   ```

2. **Use smaller model**:
   ```yaml
   detection:
     model: "yolov8n.pt"
   ```

3. **Lower resolution**:
   ```yaml
   detection:
     imgsz: 480
   ```

### For Better Accuracy

1. **Use larger model**:
   ```yaml
   detection:
     model: "yolov8m.pt"
   ```

2. **Lower threshold**:
   ```yaml
   detection:
     confidence_threshold: 0.3
   ```

## 🐛 Common Issues

### Issue: "CUDA not available"

**Solution**: Use CPU mode
```bash
python main.py --device cpu
```

### Issue: Low FPS

**Solutions**:
- Close other applications
- Use smaller model (yolov8n)
- Reduce image size (imgsz: 480)
- Disable stabilization

### Issue: No tracks detected

**Solutions**:
- Check video file exists
- Lower confidence threshold
- Ensure video has visible objects
- Check backend logs

## 📝 Manual Setup (Alternative)

If batch files don't work:

### Backend

```bash
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py --video data/sample.mp4 --device cpu
```

### Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env
echo VITE_API_URL=http://localhost:8000 > .env

# Run
npm run dev
```

## 🔄 Updating

```bash
# Pull latest code
git pull

# Reinstall dependencies
start_local.bat

# Restart system
start_all.bat
```

## 📚 Additional Resources

- **Full Documentation**: README.md
- **API Reference**: API.md
- **Troubleshooting**: TROUBLESHOOTING.md
- **Frontend Guide**: FRONTEND_SETUP.md

## 🆘 Getting Help

1. Check TROUBLESHOOTING.md
2. Review logs in `daemon_vision.log`
3. Check browser console (F12)
4. Contact Core team

## ✅ Checklist

Before running:
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Video file in `data/sample.mp4` (optional)
- [ ] Ran `start_local.bat`
- [ ] Ports 8000 and 3000 are free

To run:
- [ ] Double-click `start_all.bat`
- [ ] Wait for both windows to open
- [ ] Open http://localhost:3000 in browser
- [ ] See tracks appearing in real-time

## 🎯 Next Steps

1. **Test with your video**: Add video to `data/` folder
2. **Customize settings**: Edit `config.yaml`
3. **Explore API**: Visit http://localhost:8000/docs
4. **Run tests**: `python test_integration.py`

---

**Need help?** Check TROUBLESHOOTING.md or contact the team.

**System working?** You're ready to go! 🚀
