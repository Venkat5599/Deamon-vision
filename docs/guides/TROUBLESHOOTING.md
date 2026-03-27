# Daemon Vision - Troubleshooting Guide

## Docker Issues

### Error: "unable to get image" or "cannot find pipe"

**Problem**: Docker Desktop is not running

**Solutions**:

1. **Start Docker Desktop**:
   - Open Docker Desktop application
   - Wait for it to fully start (whale icon should be steady)
   - Run: `docker-compose up --build`

2. **Use Local Development Instead**:
   ```bash
   # Run setup
   start_local.bat
   
   # Start both backend and frontend
   start_all.bat
   ```

### Error: "version is obsolete"

**Problem**: Docker Compose warning about version field

**Solution**: This is just a warning, ignore it. Or remove the `version: '3.8'` line from `docker-compose.yml`

### Error: "CUDA not available"

**Problem**: No GPU or NVIDIA drivers not installed

**Solution**: Run on CPU instead:
```bash
python main.py --video data/sample.mp4 --device cpu
```

## Backend Issues

### Error: "No module named 'ultralytics'"

**Problem**: Dependencies not installed

**Solution**:
```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Error: "Video file not found"

**Problem**: No video file in data/ folder

**Solutions**:

1. **Add a video file**:
   - Place any MP4/AVI video in `data/sample.mp4`
   - Or download sample: [link to drone footage]

2. **Use simulated data**:
   - System will auto-generate simulated telemetry
   - Detection will work on any video

### Error: "Failed to load YOLO model"

**Problem**: Model not downloaded

**Solution**:
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Error: "Port 8000 already in use"

**Problem**: Another process using port 8000

**Solution**:
```bash
# Windows: Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in config.yaml
api:
  port: 8001
```

## Frontend Issues

### Error: "npm not found"

**Problem**: Node.js not installed

**Solution**:
1. Download Node.js 18+ from https://nodejs.org/
2. Install and restart terminal
3. Run: `npm --version` to verify

### Error: "Cannot connect to backend"

**Problem**: Backend not running or wrong URL

**Solutions**:

1. **Check backend is running**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check .env file**:
   ```bash
   # frontend/.env
   VITE_API_URL=http://localhost:8000
   ```

3. **Check CORS settings** in `config.yaml`:
   ```yaml
   api:
     cors_origins: ["*"]
   ```

### Error: "WebSocket connection failed"

**Problem**: WebSocket endpoint not accessible

**Solutions**:

1. **Check backend logs** for WebSocket errors
2. **Test WebSocket directly**:
   ```bash
   # Install wscat
   npm install -g wscat
   
   # Test connection
   wscat -c ws://localhost:8000/stream
   ```

3. **Check firewall** isn't blocking port 8000

### Error: "Module not found" in frontend

**Problem**: Dependencies not installed

**Solution**:
```bash
cd frontend
npm install
```

## Performance Issues

### Low FPS (<15)

**Solutions**:

1. **Use smaller model**:
   ```yaml
   # config.yaml
   detection:
     model: "yolov8n.pt"  # Smallest, fastest
   ```

2. **Reduce image size**:
   ```yaml
   detection:
     imgsz: 480  # Lower resolution
   ```

3. **Use GPU**:
   ```bash
   python main.py --device cuda
   ```

4. **Disable stabilization**:
   ```yaml
   sensor:
     enable_stabilization: false
   ```

### High Memory Usage

**Solutions**:

1. **Reduce trajectory history**:
   ```yaml
   tracking:
     trajectory_history: 15  # Lower value
   ```

2. **Reduce track buffer**:
   ```yaml
   tracking:
     track_buffer: 30  # Lower value
   ```

3. **Close other applications**

### High ID Switch Rate

**Solutions**:

1. **Increase IoU threshold**:
   ```yaml
   tracking:
     match_thresh: 0.9  # Higher = stricter
   ```

2. **Increase track buffer**:
   ```yaml
   tracking:
     track_buffer: 120  # Keep tracks longer
   ```

## Windows-Specific Issues

### Error: "python not found"

**Solution**:
```bash
# Use py instead
py --version
py -m venv venv
```

### Error: "Scripts\activate.bat not found"

**Solution**:
```bash
# Use full path
venv\Scripts\activate.bat

# Or use PowerShell
venv\Scripts\Activate.ps1
```

### Error: "Permission denied"

**Solution**:
```bash
# Run as Administrator
# Right-click Command Prompt -> Run as Administrator
```

## Quick Diagnostics

### Check System Status

```bash
# Backend health
curl http://localhost:8000/health

# Frontend accessibility
curl http://localhost:3000

# WebSocket
wscat -c ws://localhost:8000/stream
```

### Check Logs

```bash
# Backend logs
tail -f daemon_vision.log

# Docker logs
docker logs daemon-vision
docker logs daemon-vision-frontend
```

### Check Ports

```bash
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Check if ports are free
```

## Common Error Messages

### "CUDA out of memory"

**Solution**: Use CPU or smaller model
```bash
python main.py --device cpu
```

### "Connection refused"

**Solution**: Backend not running, start it first

### "Module 'cv2' has no attribute 'VideoCapture'"

**Solution**: Reinstall OpenCV
```bash
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python==4.8.1.78
```

### "WebSocket closed unexpectedly"

**Solution**: Check backend logs, may be crashing

## Getting Help

### Collect Debug Information

```bash
# System info
python --version
node --version
docker --version

# Backend status
curl http://localhost:8000/health

# Check logs
type daemon_vision.log
```

### Report Issues

Include:
1. Error message (full text)
2. System info (OS, Python version, Node version)
3. Steps to reproduce
4. Logs (daemon_vision.log)

## Quick Fixes

### Reset Everything

```bash
# Stop all processes
taskkill /F /IM python.exe
taskkill /F /IM node.exe

# Clean up
rmdir /s /q venv
rmdir /s /q frontend\node_modules
rmdir /s /q frontend\dist

# Reinstall
start_local.bat
```

### Fresh Start

```bash
# Pull latest code
git pull

# Rebuild
docker-compose down
docker-compose up --build

# Or local
start_local.bat
start_all.bat
```

## Still Having Issues?

1. Check this guide thoroughly
2. Review logs carefully
3. Try fresh installation
4. Contact Core team with debug info

---

**Most issues are solved by:**
1. Ensuring Docker Desktop is running
2. Installing all dependencies
3. Using correct ports (8000, 3000)
4. Running backend before frontend
