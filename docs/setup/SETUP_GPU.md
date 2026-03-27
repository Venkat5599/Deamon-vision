# 🚀 GPU Setup Guide - RTX 4060

## Step 1: Download Python 3.11

1. Go to: https://www.python.org/downloads/
2. Download **Python 3.11.9** (latest 3.11 version)
3. Run the installer
4. ✅ **IMPORTANT**: Check "Add Python 3.11 to PATH"
5. Click "Install Now"

## Step 2: Verify Python 3.11 Installation

Open a NEW PowerShell window and run:
```bash
python3.11 --version
```

Should show: `Python 3.11.9`

## Step 3: Create New Virtual Environment

Run these commands in your project folder:

```bash
# Create new venv with Python 3.11
python3.11 -m venv venv311

# Activate it
.\venv311\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel
```

## Step 4: Install PyTorch with CUDA

```bash
# Install PyTorch with CUDA 11.8 support
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Step 5: Install Other Dependencies

```bash
# Install all other packages
pip install ultralytics fastapi uvicorn websockets python-multipart
pip install opencv-python pillow pyyaml numpy scipy filterpy lap
```

## Step 6: Verify GPU is Working

```bash
python check_cuda.py
```

Should show:
```
CUDA available: True
CUDA version: 11.8
Device count: 1
Device name: NVIDIA GeForce RTX 4060
```

## Step 7: Run with GPU!

```bash
python main.py --device cuda
```

## Expected Performance

- **CPU**: ~7-15 FPS
- **GPU (RTX 4060)**: ~60-120 FPS 🚀

Your video will be MUCH smoother!

## Troubleshooting

### Python 3.11 not found?
- Make sure you checked "Add to PATH" during installation
- Restart PowerShell after installing
- Try: `py -3.11 -m venv venv311`

### CUDA still not available?
- Make sure you have NVIDIA drivers installed
- Update drivers from: https://www.nvidia.com/download/index.aspx
- Restart computer after driver update

### Import errors?
- Make sure venv311 is activated (you should see `(venv311)` in prompt)
- Reinstall packages if needed

## Quick Commands Summary

```bash
# 1. Create venv
python3.11 -m venv venv311

# 2. Activate
.\venv311\Scripts\Activate.ps1

# 3. Install PyTorch with CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 4. Install dependencies
pip install ultralytics fastapi uvicorn websockets python-multipart opencv-python pillow pyyaml numpy scipy filterpy lap

# 5. Check GPU
python check_cuda.py

# 6. Run with GPU!
python main.py --device cuda
```

Ready to go! 🎯
