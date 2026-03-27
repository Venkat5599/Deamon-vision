# Video Upload Feature Guide

## Overview
You can now upload video files directly from the frontend interface! No need to manually place files in the `data/` folder.

## How to Upload a Video

### Method 1: Frontend Upload (Recommended)
1. Open the frontend at **http://localhost:3001**
2. Look for the **upload icon** (📤) in the top-right header
3. Click the upload icon
4. Select your video file (MP4, AVI, MOV, or MKV)
5. The video will be uploaded and processing will start automatically
6. You'll see a confirmation message when upload is complete

### Method 2: Manual File Placement
1. Place your video file in the `data/` folder
2. Rename it to `sample.mp4` (or update `config.yaml`)
3. Restart the backend

## Supported Video Formats
- MP4 (recommended)
- AVI
- MOV
- MKV

## Current Setup
- **Frontend**: Running on http://localhost:3001
- **Backend**: Running on http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Video Source**: Webcam (camera index 0) by default

## Using Webcam
The system is currently configured to use your webcam. If you want to test with your webcam:
1. Make sure your webcam is connected
2. The backend should already be detecting from camera 0
3. Open http://localhost:3001 to see the live feed

## Switching Between Sources

### To use uploaded video:
Just upload a video through the frontend - it will automatically switch!

### To use webcam:
Edit `config.yaml` and set:
```yaml
sensor:
  video_source: 0  # 0 for default webcam, 1 for second camera, etc.
```

### To use a specific file:
Edit `config.yaml` and set:
```yaml
sensor:
  video_source: "data/your_video.mp4"
```

## API Endpoint
You can also upload videos programmatically:
```bash
curl -X POST http://localhost:8000/upload/video \
  -F "file=@your_video.mp4"
```

## Troubleshooting

### Upload button not visible
- Make sure frontend is running on port 3001
- Check browser console for errors
- Refresh the page

### Upload fails
- Check file size (keep under 500MB for best performance)
- Verify file format is supported
- Check backend logs for errors

### Video not processing after upload
- Check backend terminal for errors
- Verify backend is running on port 8000
- Try restarting the backend

## Next Steps
1. Upload a video or use your webcam
2. Watch real-time object detection and tracking
3. Click on detected objects to lock onto them
4. Use keyboard shortcuts:
   - `T` - Toggle trajectories
   - `U` - Unlock target
   - `1-9` - Quick lock to track ID

## Performance Tips
- Use shorter videos (30-60 seconds) for testing
- Lower resolution videos process faster
- CPU mode is slower but works without GPU
- For best performance, use a GPU-enabled system

Enjoy your tactical surveillance system! 🎯
