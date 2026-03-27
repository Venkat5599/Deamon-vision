# 🚀 Install Everything via Commands

## Option 1: Using winget (Windows 11/10)

```bash
# Install Python 3.11
winget install Python.Python.3.11

# Restart PowerShell, then run setup
.\setup_gpu.bat
```

## Option 2: Using Chocolatey

```bash
# Install Chocolatey first (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Python 3.11
choco install python311 -y

# Restart PowerShell, then run setup
.\setup_gpu.bat
```

## Option 3: All-in-One Script (Manual Commands)

Just copy and paste these commands one by one:

```bash
# 1. Install Python 3.11 (using winget)
winget install Python.Python.3.11

# 2. Close and reopen PowerShell, then continue:

# 3. Create Python 3.11 environment
python3.11 -m venv venv311

# 4. Activate it
.\venv311\Scripts\Activate.ps1

# 5. Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# 6. Install PyTorch with CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 7. Install other dependencies
pip install ultralytics fastapi uvicorn websockets python-multipart opencv-python pillow pyyaml numpy scipy filterpy lap

# 8. Verify GPU
python check_cuda.py

# 9. Run with GPU!
python main.py --device cuda
```

## Quick Check: Is winget available?

```bash
winget --version
```

If you see a version number, you have winget! Use Option 1.

If not, use Option 2 (Chocolatey) or download manually from python.org.

## After Python 3.11 is Installed

Just run:
```bash
.\setup_gpu.bat
```

This will do steps 3-8 automatically!

---

**Fastest way**: Run `winget install Python.Python.3.11`, restart PowerShell, then run `.\setup_gpu.bat`
