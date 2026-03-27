# ✅ GPU Setup Checklist

## Before You Start

- [ ] You have Windows with PowerShell
- [ ] You have RTX 4060 GPU
- [ ] You have internet connection
- [ ] You have admin rights (for Python installation)

## Step 1: Install Python 3.11 (5 minutes)

- [ ] Go to https://www.python.org/downloads/
- [ ] Download Python 3.11.9
- [ ] Run installer
- [ ] ✅ CHECK "Add Python 3.11 to PATH"
- [ ] Click "Install Now"
- [ ] Close all PowerShell windows
- [ ] Open NEW PowerShell
- [ ] Run: `python3.11 --version`
- [ ] Should show: `Python 3.11.9`

## Step 2: Run Setup Script (10-15 minutes)

- [ ] Open PowerShell in your project folder
- [ ] Run: `.\setup_gpu.bat`
- [ ] Wait for installation (downloads ~2GB)
- [ ] Check output shows: "CUDA available: True"
- [ ] Check output shows: "Device name: NVIDIA GeForce RTX 4060"
- [ ] See "Setup Complete!" message

## Step 3: Start Backend with GPU (1 minute)

- [ ] In PowerShell, run: `.\venv311\Scripts\Activate.ps1`
- [ ] Should see `(venv311)` in prompt
- [ ] Run: `python main.py --device cuda`
- [ ] Check logs show: "Using device: cuda"
- [ ] Check logs show: "Model loaded on NVIDIA GeForce RTX 4060"
- [ ] Backend running on http://localhost:8000

## Step 4: Start Frontend (1 minute)

- [ ] Open NEW PowerShell window
- [ ] Run: `cd frontend`
- [ ] Run: `npm run dev`
- [ ] Frontend running on http://localhost:3001

## Step 5: Test It! (1 minute)

- [ ] Open browser: http://localhost:3001
- [ ] See video feed with bounding boxes
- [ ] Video plays smoothly (no stuttering)
- [ ] See track IDs and confidence scores
- [ ] See metrics dashboard updating
- [ ] FPS counter shows 60-120 FPS

## Verification

### Check GPU Usage:
- [ ] Open Task Manager (Ctrl+Shift+Esc)
- [ ] Go to Performance tab
- [ ] Click on GPU
- [ ] Should see 40-60% usage while processing

### Check Backend Logs:
- [ ] See "Using device: cuda"
- [ ] See "Model loaded on NVIDIA GeForce RTX 4060"
- [ ] See "Processing frame" messages
- [ ] No errors or warnings

### Check Frontend:
- [ ] Video displays smoothly
- [ ] Bounding boxes track cars
- [ ] Track IDs stay consistent
- [ ] Metrics update in real-time
- [ ] No lag or stuttering

## Success Criteria

✅ Backend logs show "Using device: cuda"
✅ GPU usage in Task Manager shows 40-60%
✅ Video plays smoothly at 60-120 FPS
✅ No stuttering or lag
✅ Bounding boxes track cars accurately
✅ Track IDs stay consistent

## If Something Goes Wrong

### Python 3.11 not found?
→ Read: INSTALL_PYTHON_311.md

### CUDA not available?
→ Update NVIDIA drivers
→ Restart computer
→ Run check_cuda.py again

### Still slow?
→ Make sure you're in venv311
→ Make sure you used --device cuda
→ Check GPU usage in Task Manager

### Need help?
→ Read: GPU_SETUP_COMPLETE.md
→ Read: SETUP_GPU.md

## Time Estimate

- Python 3.11 installation: 5 minutes
- Setup script: 10-15 minutes
- Testing: 5 minutes
- **Total: ~20-25 minutes**

## What You'll Get

- **Before**: 7-15 FPS, stuttering video
- **After**: 60-120 FPS, smooth video
- **Improvement**: 4-8x faster! 🚀

---

Ready? Start with Step 1! 🎯
