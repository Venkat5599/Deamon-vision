# 📥 How to Install Python 3.11

## Step 1: Download

1. Go to: **https://www.python.org/downloads/**
2. Look for **Python 3.11.9** (or latest 3.11.x)
3. Click the download button

## Step 2: Install

1. Run the installer
2. ⚠️ **IMPORTANT**: Check the box that says **"Add Python 3.11 to PATH"**
3. Click **"Install Now"**
4. Wait for installation to complete
5. Click **"Close"**

## Step 3: Verify

1. **Close all PowerShell windows**
2. Open a **NEW** PowerShell window
3. Run this command:

```bash
python3.11 --version
```

You should see:
```
Python 3.11.9
```

## Step 4: Run Setup Script

Now you're ready! Run:

```bash
.\setup_gpu.bat
```

This will automatically:
- Create a Python 3.11 virtual environment
- Install PyTorch with CUDA support for your RTX 4060
- Install all other dependencies
- Verify your GPU is working

## Alternative: If python3.11 command doesn't work

Try this instead:

```bash
py -3.11 --version
```

If that works, modify the setup script to use `py -3.11` instead of `python3.11`.

## Need Help?

If you get stuck:
1. Make sure you checked "Add to PATH" during installation
2. Restart your computer
3. Try the installation again

---

Once Python 3.11 is installed, just run `.\setup_gpu.bat` and you're done! 🎉
