# 🎯 START HERE - GPU Setup for RTX 4060

## Option 1: Automatic Setup (Recommended)

Just run this script and it will do everything:

```bash
.\setup_gpu.bat
```

That's it! The script will:
- Create Python 3.11 environment
- Install PyTorch with CUDA
- Install all dependencies
- Verify your GPU
- Tell you how to run

## Option 2: Manual Setup

If you prefer to run commands yourself:

### 1. Install Python 3.11
- Download from: https://www.python.org/downloads/
- Install and check "Add to PATH"
- Restart PowerShell

### 2. Run these commands:

```bash
# Create environment
python3.11 -m venv venv311

# Activate it
.\venv311\Scripts\Activate.ps1

# Install PyTorch with CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Install other packages
pip install ultralytics fastapi uvicorn websockets python-multipart opencv-python pillow pyyaml numpy scipy filterpy lap

# Check GPU
python check_cuda.py

# Run with GPU!
python main.py --device cuda
```

## What to Expect

When you run `python check_cuda.py`, you should see:
```
CUDA available: True
CUDA version: 11.8
Device count: 1
Device name: NVIDIA GeForce RTX 4060
```

## Performance

- **Before (CPU)**: ~7-15 FPS 🐌
- **After (GPU)**: ~60-120 FPS 🚀

Your racing video will be SMOOTH!

## Running the System

### Backend (with GPU):
```bash
.\venv311\Scripts\Activate.ps1
python main.py --device cuda
```

### Frontend (separate terminal):
```bash
cd frontend
npm run dev
```

Then open: http://localhost:3001

## Troubleshooting

### "python3.11 not found"
- Install Python 3.11 from python.org
- Make sure you checked "Add to PATH"
- Restart PowerShell

### "CUDA available: False"
- Update NVIDIA drivers: https://www.nvidia.com/download/index.aspx
- Restart computer
- Run check_cuda.py again

### Still having issues?
Check the detailed guide: `SETUP_GPU.md`

---

Ready? Run `.\setup_gpu.bat` and let's go! 🚀
