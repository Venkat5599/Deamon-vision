# 🚀 Quick GPU Setup - 5 Minutes

## What You Need
1. Download Python 3.11.9 from: https://www.python.org/downloads/
2. Install it (check "Add to PATH")
3. Restart PowerShell

## Run These Commands

```bash
# 1. Create Python 3.11 environment
python3.11 -m venv venv311

# 2. Activate it
.\venv311\Scripts\Activate.ps1

# 3. Install PyTorch with CUDA (this is the important one!)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 4. Install everything else
pip install ultralytics fastapi uvicorn websockets python-multipart opencv-python pillow pyyaml numpy scipy filterpy lap

# 5. Verify GPU works
python check_cuda.py

# 6. Run with GPU!
python main.py --device cuda
```

## Expected Output from check_cuda.py
```
CUDA available: True
CUDA version: 11.8
Device count: 1
Device name: NVIDIA GeForce RTX 4060
```

## Performance Boost
- CPU: ~7-15 FPS 🐌
- GPU: ~60-120 FPS 🚀

Your racing video will be SMOOTH! 🏎️
