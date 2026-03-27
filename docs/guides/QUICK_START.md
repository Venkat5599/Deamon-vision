# 🚀 Quick Start Guide

## Current Status

- ✅ Frontend: Running on http://localhost:3001
- ⚠️ Backend: Needs video source to stay running
- ✅ All dependencies installed
- ✅ UI fully integrated

## Start Everything

### 1. Open Frontend
```
http://localhost:3001
```

**IMPORTANT**: Press **Ctrl + Shift + R** to hard refresh and clear cache!

### 2. Upload a Video

Click the "Upload Video" button in the top-right corner and select any video file (MP4, AVI, MOV).

The backend will automatically:
- Receive your video
- Start processing it
- Send real-time tracking data to the frontend
- Display detections on the video feed

## What You'll See

Once a video is uploaded:

1. **Header** - Connection status turns green, FPS/latency metrics appear
2. **Video Feed** - Your video with bounding boxes around detected objects
3. **Track List** - Sidebar showing all detected objects with details
4. **Metrics** - Bottom panel with system performance stats
5. **Interactive** - Click on objects to lock onto them

## Keyboard Shortcuts

- `T` - Toggle trajectories on/off
- `U` - Unlock all targets
- `1-9` - Quick lock to track ID 1-9
- Click on video - Lock nearest object

## Features to Try

1. **Upload Video** - Click upload button, select video
2. **Lock Target** - Click on a detected object or press 1-9
3. **View Metrics** - Check FPS, latency, confidence scores
4. **Toggle Trajectories** - Press T to show/hide movement paths
5. **Unlock** - Press U or click the lock icon

## Troubleshooting

### Frontend shows plain HTML?
- Press **Ctrl + Shift + R** (hard refresh)
- Clear browser cache
- Check console (F12) for errors

### Backend not responding?
- Upload a video through the frontend
- Backend will start processing automatically

### No detections showing?
- Make sure video has people, cars, or other objects
- Check that backend is processing (look for FPS > 0)
- Try a different video

## System Requirements

- **Browser**: Chrome, Edge, or Firefox (latest version)
- **Python**: 3.10+ with all dependencies installed
- **Video**: MP4, AVI, MOV format recommended
- **Objects**: People, cars, trucks, buses, motorcycles, bicycles, airplanes

## What's Integrated

✅ Real-time object detection (YOLOv8)
✅ Multi-target tracking (ByteTrack)
✅ Target locking system
✅ WebSocket streaming
✅ Video upload
✅ Beautiful modern UI
✅ Performance metrics
✅ Keyboard shortcuts
✅ Toast notifications
✅ Responsive design

## Next Steps

1. Open http://localhost:3001
2. Hard refresh (Ctrl + Shift + R)
3. Upload a video
4. Watch the magic happen! 🎯

Enjoy your tactical surveillance system!
