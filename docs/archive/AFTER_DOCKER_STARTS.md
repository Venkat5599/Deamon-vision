# What to Do After Docker Starts

## ✅ Docker is Running - Now What?

### Step 1: Verify Services are Running

Open browser and check:

1. **Frontend**: http://localhost:3000
   - Should show tactical dark interface
   - "DAEMON VISION" header at top

2. **Backend API**: http://localhost:8000/docs
   - Should show FastAPI documentation
   - Interactive API explorer

3. **Health Check**: http://localhost:8000/health
   - Should return: `{"status": "healthy"}`

### Step 2: Add a Video File

**Important**: The system needs a video to process!

1. Get any video file (MP4, AVI, MOV)
2. Rename it to `sample.mp4`
3. Place it here:
   ```
   C:\Users\ksubh\OneDrive\Documents\Palanateir\data\sample.mp4
   ```

4. Restart backend:
   ```bash
   docker-compose restart daemon-vision
   ```

**No video?** System will use simulated data, but you won't see real detections.

### Step 3: Use the Interface

Open http://localhost:3000 and you'll see:

#### **Main Screen Layout**

```
┌─────────────────────────────────────────────────────┐
│ DAEMON VISION | System Status | FPS | Latency       │
├──────┬──────────────────────────────────┬───────────┤
│      │                                  │           │
│ SIDE │  VIDEO FEED                      │  TRACK    │
│ BAR  │  (with bounding boxes)           │  LIST     │
│      │                                  │           │
├──────┴──────────────────────────────────┴───────────┤
│  METRICS: FPS Chart | Tracks | Latency               │
└─────────────────────────────────────────────────────┘
```

#### **Controls**

- **Click "LOCK" button** on track card → Lock onto target
- **Click on video** → Lock nearest track
- **Press T** → Toggle trajectory lines
- **Press U** → Unlock current target
- **Press 1-9** → Lock track by ID number

#### **Track Colors**

- 🟢 **Green**: Active track (good confidence)
- 🔴 **Red**: Locked target
- 🟡 **Yellow**: Low confidence
- ⚫ **Gray**: Lost track

### Step 4: Test the System

#### **Test 1: Check Tracks**

```bash
curl http://localhost:8000/tracks
```

Should return JSON with active tracks.

#### **Test 2: Lock a Target**

In the UI:
1. Wait for tracks to appear
2. Click "LOCK" on any track card
3. Track should turn red
4. Gimbal delta shown in metrics

#### **Test 3: WebSocket**

Open browser console (F12) and check:
- WebSocket connection status
- Real-time track updates
- No errors

### Step 5: Monitor Performance

Check the metrics dashboard (bottom of screen):

- **FPS**: Should be 15-30 FPS
- **Latency**: Should be 50-100ms
- **Active Tracks**: Number of detected objects

### Common Issues After Start

#### Issue: "No tracks appearing"

**Solutions**:
1. Add a video file to `data/sample.mp4`
2. Restart backend: `docker-compose restart daemon-vision`
3. Check video has moving objects
4. Lower confidence threshold in `config.yaml`

#### Issue: "Frontend shows 'OFFLINE'"

**Solutions**:
1. Check backend is running: `docker ps`
2. Check backend health: `curl http://localhost:8000/health`
3. Check logs: `docker logs daemon-vision`
4. Restart: `docker-compose restart`

#### Issue: "Low FPS (<10)"

**Solutions**:
1. System is using CPU (no GPU detected)
2. This is normal without NVIDIA GPU
3. Add video with fewer objects
4. Reduce image size in `config.yaml`

### Step 6: View Logs

To see what's happening:

```bash
# All logs
docker-compose logs -f

# Backend only
docker logs daemon-vision -f

# Frontend only
docker logs daemon-vision-frontend -f
```

### Step 7: Stop the System

When done:

```bash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Step 8: Restart Later

Next time you want to use it:

```bash
# Start (much faster, ~30 seconds)
docker-compose up -d

# Check status
docker ps

# View logs
docker-compose logs -f
```

## 🎯 Quick Commands Reference

```bash
# Start system
docker-compose up -d

# Stop system
docker-compose down

# Restart backend
docker-compose restart daemon-vision

# Restart frontend
docker-compose restart daemon-vision-frontend

# View logs
docker-compose logs -f

# Check status
docker ps

# Access shell in backend
docker exec -it daemon-vision bash

# Run tests
docker exec -it daemon-vision python test_integration.py
```

## 🎮 Keyboard Shortcuts in UI

| Key | Action |
|-----|--------|
| T | Toggle trajectories |
| U | Unlock target |
| 1-9 | Lock track by ID |
| Click | Lock nearest track |

## 📊 Expected Performance

| Metric | With GPU | Without GPU (CPU) |
|--------|----------|-------------------|
| FPS | 25-30 | 5-15 |
| Latency | 50-70ms | 100-200ms |
| Memory | 2GB GPU | 1GB RAM |

## 🆘 Need Help?

1. Check logs: `docker-compose logs -f`
2. Check TROUBLESHOOTING.md
3. Check browser console (F12)
4. Restart: `docker-compose restart`

## ✅ Success Checklist

- [ ] Frontend loads at http://localhost:3000
- [ ] Backend API at http://localhost:8000/docs
- [ ] Health check returns "healthy"
- [ ] Video file added to data/sample.mp4
- [ ] Tracks appearing in UI
- [ ] Can lock/unlock targets
- [ ] Metrics showing FPS and latency

**All checked?** You're ready to go! 🚀

---

**Enjoy your tactical surveillance system!**
