# YOLO Model Comparison for Your RTX 4060

## Current Setup: YOLOv8s (Recommended)

| Model | Speed (FPS) | Accuracy | GPU Memory | Best For |
|-------|-------------|----------|------------|----------|
| **yolov8n** | ~80-100 | Good | ~1GB | Speed priority |
| **yolov8s** ⭐ | ~50-70 | Better | ~2GB | **Balanced (CURRENT)** |
| yolov8m | ~30-40 | Great | ~4GB | Accuracy priority |
| yolov8l | ~20-25 | Excellent | ~6GB | Maximum accuracy |
| yolov8x | ~15-20 | Best | ~8GB | Research/offline |

## What Changed

### Before (yolov8n):
- Model: Nano (smallest, fastest)
- Confidence: 0.5 (50%)
- Image size: 416px
- Result: Fast but misses some cars

### After (yolov8s):
- Model: Small (balanced)
- Confidence: 0.3 (30%)
- Image size: 640px
- Result: More accurate, catches more cars

## Performance Impact

With RTX 4060:
- **yolov8n**: ~80-100 FPS detection
- **yolov8s**: ~50-70 FPS detection (still very fast!)
- **Pipeline**: Should still run at 6-10 FPS overall

## If You Want Even More Accuracy

Edit `config.yaml`:

```yaml
detection:
  model: "yolov8m.pt"  # Medium model
  confidence_threshold: 0.25
  imgsz: 640
```

This will:
- Detect even more objects
- Better accuracy on small/distant cars
- Slower: ~30-40 FPS detection
- Uses more GPU memory (~4GB)

## If You Want Maximum Speed

Edit `config.yaml`:

```yaml
detection:
  model: "yolov8n.pt"  # Nano model
  confidence_threshold: 0.4
  imgsz: 416
```

This will:
- Maximum speed: ~80-100 FPS
- Good enough for most cases
- Minimal GPU memory

## Restart After Changes

```bash
# Stop backend
Ctrl+C

# Start with new model
.\venv311\Scripts\Activate.ps1
python main.py --device cuda
```

The model will download automatically on first run!

---

**Current config is optimized for your racing video!** 🏎️
