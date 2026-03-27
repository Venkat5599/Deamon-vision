# 🚀 ONE COMMAND SETUP

## The Fastest Way (You Have winget!)

### Option 1: Two Commands (Recommended)

```bash
# 1. Install Python 3.11
winget install Python.Python.3.11

# 2. Close PowerShell, open new one, then run:
.\setup_gpu.bat
```

### Option 2: Fully Automated

```bash
.\install_all.ps1
```

This will:
1. Install Python 3.11 via winget
2. Create venv311
3. Install PyTorch with CUDA
4. Install all dependencies
5. Verify GPU
6. Done!

## Manual Commands (If You Prefer)

```bash
# Install Python 3.11
winget install Python.Python.3.11

# Close and reopen PowerShell, then:
python3.11 -m venv venv311
.\venv311\Scripts\Activate.ps1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install ultralytics fastapi uvicorn websockets python-multipart opencv-python pillow pyyaml numpy scipy filterpy lap
python check_cuda.py
python main.py --device cuda
```

## What Each Script Does

| Script | What It Does |
|--------|--------------|
| `install_all.ps1` | Installs Python 3.11 + sets up everything |
| `setup_gpu.bat` | Sets up GPU (requires Python 3.11 already installed) |
| `check_cuda.py` | Verifies GPU is working |

## Recommended Flow

```bash
# Step 1: Install Python 3.11
winget install Python.Python.3.11

# Step 2: Close PowerShell and open new one

# Step 3: Run setup
.\setup_gpu.bat

# Step 4: Run with GPU
.\venv311\Scripts\Activate.ps1
python main.py --device cuda
```

## Why Two Steps?

Windows needs to refresh the PATH after installing Python. That's why you need to close and reopen PowerShell after the winget install.

## Time Estimate

- `winget install`: 2-3 minutes
- `setup_gpu.bat`: 10-15 minutes
- **Total**: ~15 minutes

## Expected Output

After `python check_cuda.py`:
```
CUDA available: True
CUDA version: 11.8
Device count: 1
Device name: NVIDIA GeForce RTX 4060
```

After `python main.py --device cuda`:
```
Using device: cuda
Model loaded on NVIDIA GeForce RTX 4060
Processing at 60-120 FPS 🚀
```

---

**Ready?** Just run:
```bash
winget install Python.Python.3.11
```

Then close PowerShell, open new one, and run:
```bash
.\setup_gpu.bat
```

That's it! 🎉
