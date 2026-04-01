# Model Weights

## Why Model Files Are Not in the Repository

The `.pt` (PyTorch) model weight files are **NOT included in this repository** because:

1. **Large file size**: 6.2 MB (yolov8n.pt) - would bloat the Git repository
2. **Automatic download**: Ultralytics YOLO automatically downloads models on first use
3. **Version control**: Models are versioned by Ultralytics, not by us
4. **Best practice**: Model weights should be stored separately (Git LFS, cloud storage, or auto-download)

## How to Get the Model Weights

### Option 1: Automatic Download (Recommended)

The model is **automatically downloaded** when you first run the system:

```bash
# Just run the system - model downloads automatically
python start_with_video.py
```

The first time you run it, you'll see:
```
Downloading yolov8n.pt from https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt...
```

The model is saved to the project root directory.

### Option 2: Manual Download

If you want to download the model manually:

**YOLOv8n (Nano - 6.2 MB)**
```bash
# Using wget
wget https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt

# Using curl
curl -L https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt -o yolov8n.pt

# Using Python
from ultralytics import YOLO
model = YOLO('yolov8n.pt')  # Downloads automatically
```

**Direct Download Link**: https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt

### Option 3: Other YOLOv8 Variants

If you want different model sizes:

| Model | Size | mAP | Speed | Download Link |
|-------|------|-----|-------|---------------|
| YOLOv8n | 6.2 MB | 37.3% | Fastest | [Download](https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt) |
| YOLOv8s | 22 MB | 44.9% | Fast | [Download](https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8s.pt) |
| YOLOv8m | 52 MB | 50.2% | Medium | [Download](https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8m.pt) |
| YOLOv8l | 87 MB | 52.9% | Slow | [Download](https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8l.pt) |
| YOLOv8x | 136 MB | 53.9% | Slowest | [Download](https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8x.pt) |

**We use YOLOv8n** because it's the fastest and perfect for real-time drone applications.

## Model Location

After download, the model should be in the project root:

```
Deamon-vision/
├── yolov8n.pt          ← Model file (auto-downloaded)
├── config.yaml         ← Points to yolov8n.pt
├── src/
├── frontend/
└── ...
```

## Verifying Model Download

Check if the model exists:

```bash
# Windows PowerShell
Test-Path yolov8n.pt

# Linux/Mac
ls -lh yolov8n.pt
```

Expected output:
```
-rw-r--r-- 1 user user 6.2M Mar 27 15:00 yolov8n.pt
```

## Model Information

### YOLOv8n Specifications

- **File**: yolov8n.pt
- **Size**: 6,549,796 bytes (6.2 MB)
- **Architecture**: YOLOv8 Nano
- **Parameters**: 3.2M
- **Training Dataset**: COCO (330K images, 80 classes)
- **Input Size**: 640x640
- **Classes**: 80 (person, car, truck, bus, bicycle, etc.)
- **Format**: PyTorch (.pt)

### Model Hash (for verification)

If you want to verify the downloaded model:

```python
import hashlib

def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

print(get_file_hash('yolov8n.pt'))
```

## Using Different Models

To use a different YOLOv8 variant, update `config.yaml`:

```yaml
detection:
  model: yolov8s.pt  # Change from yolov8n.pt to yolov8s.pt
  # ... other settings
```

Then download the new model:
```bash
wget https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8s.pt
```

## For Your Friend

**Tell your friend:**

1. **The model is NOT in the repo** - it's auto-downloaded
2. **To get it**: Just run the system, or download from the link above
3. **File size**: 6.2 MB (too large for Git without LFS)
4. **Location**: Project root directory after download
5. **Source**: Official Ultralytics release (verified and safe)

## Troubleshooting

### Model Not Downloading?

If automatic download fails:

1. **Check internet connection**
2. **Download manually** using the links above
3. **Place in project root** (same folder as config.yaml)
4. **Verify filename** is exactly `yolov8n.pt`

### Model Loading Error?

```python
# Test if model loads correctly
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
print(model.names)  # Should print 80 class names
```

## Alternative: Git LFS (Optional)

If you want to include the model in the repository:

```bash
# Install Git LFS
git lfs install

# Track .pt files
git lfs track "*.pt"

# Add and commit
git add .gitattributes yolov8n.pt
git commit -m "Add model weights with Git LFS"
git push
```

**Note**: This requires Git LFS to be installed on all machines that clone the repo.

## Summary

- ✅ Model auto-downloads on first run
- ✅ 6.2 MB file (yolov8n.pt)
- ✅ Official Ultralytics release
- ✅ No manual download needed
- ✅ Can be manually downloaded if needed
- ❌ Not in Git repo (best practice)

**For most users**: Just run the system and the model downloads automatically!

---

**Model Source**: https://github.com/ultralytics/ultralytics  
**Documentation**: https://docs.ultralytics.com/models/yolov8/  
**License**: AGPL-3.0
