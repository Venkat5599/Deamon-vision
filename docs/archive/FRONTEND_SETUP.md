# Daemon Vision Frontend - Setup Guide

## 🚀 Quick Start (3 Steps)

### Option 1: Docker (Recommended)

```bash
# Start both backend and frontend
docker-compose up --build

# Access the interface
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# Terminal 1: Start backend
python main.py --video data/sample.mp4

# Terminal 2: Start frontend
cd frontend
npm install
npm run dev

# Access at http://localhost:3000
```

## 📦 What's Included

### Frontend Features
- ✅ Real-time WebSocket connection
- ✅ Live track visualization with canvas overlay
- ✅ Interactive track locking/unlocking
- ✅ Performance metrics dashboard
- ✅ Keyboard shortcuts
- ✅ Military-grade tactical UI
- ✅ Responsive design
- ✅ Auto-reconnect on disconnect

### Tech Stack
- React 18 + TypeScript
- Vite (lightning-fast builds)
- TailwindCSS (tactical design system)
- Canvas API (video overlay)
- WebSocket (real-time updates)

## 🎮 User Interface Guide

### Main Layout

```
┌─────────────────────────────────────────────────────────┐
│  HEADER: System Status, FPS, Latency                    │
├──────┬──────────────────────────────────────┬───────────┤
│      │                                      │           │
│ SIDE │  VIDEO FEED                          │  TRACK    │
│ BAR  │  (Canvas Overlay)                    │  LIST     │
│      │                                      │           │
│      │                                      │           │
├──────┴──────────────────────────────────────┴───────────┤
│  METRICS: FPS Chart | Track Density | Latency           │
├─────────────────────────────────────────────────────────┤
│  FOOTER: System Time, Status, Location                  │
└─────────────────────────────────────────────────────────┘
```

### Video Feed Panel
- **Canvas Overlay**: Shows bounding boxes, track IDs, trajectories
- **Color Coding**:
  - 🟢 Green: Active track (confidence > 50%)
  - 🔴 Red: Locked target
  - 🟡 Yellow: Low confidence (< 50%)
- **Crosshair**: Center targeting reticle
- **Corner Markers**: Tactical frame indicators

### Track List Panel
- **Track Cards**: Show all active tracks
- **Information**:
  - Track ID and class (person/vehicle/aircraft)
  - Confidence score with progress bar
  - Velocity magnitude and direction
  - Ground coordinates (lat/lon)
- **Actions**: Lock/Unlock button per track

### Metrics Dashboard
- **FPS Stability**: Real-time frame rate chart
- **Track Density**: Active tracks over time
- **Latency Histogram**: Network performance

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `T` | Toggle trajectory display |
| `U` | Unlock current target |
| `1-9` | Lock track by ID |
| Click | Lock nearest track to cursor |

## 🔧 Configuration

### Environment Variables

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

### API Endpoints

The frontend connects to these backend endpoints:

- `GET /tracks` - Fetch all active tracks
- `POST /lock/{track_id}` - Lock onto target
- `DELETE /lock` - Unlock target
- `GET /lock/status` - Get lock status
- `GET /health` - System health check
- `WS /stream` - Real-time track updates

## 🎨 Customization

### Colors

Edit `frontend/tailwind.config.js` to customize the tactical color scheme:

```javascript
colors: {
  "primary-fixed-dim": "#00e639",  // Main accent (green)
  "error": "#ffb4ab",              // Error/locked (red)
  "tertiary-fixed-dim": "#f1c100", // Warning (yellow)
  // ... more colors
}
```

### Fonts

Current fonts:
- **Headlines**: Space Grotesk (tactical, geometric)
- **Body**: Inter (readable, modern)
- **Mono**: JetBrains Mono (code, metrics)

## 🐛 Troubleshooting

### WebSocket Won't Connect

**Problem**: "SYSTEM: OFFLINE" in header

**Solutions**:
1. Check backend is running: `curl http://localhost:8000/health`
2. Verify WebSocket endpoint: `wscat -c ws://localhost:8000/stream`
3. Check CORS settings in backend `config.yaml`
4. Ensure no firewall blocking port 8000

### No Tracks Showing

**Problem**: Track list is empty

**Solutions**:
1. Verify backend has video source: Check `config.yaml`
2. Check backend logs: `docker logs daemon-vision`
3. Test API directly: `curl http://localhost:8000/tracks`
4. Ensure detection model is loaded

### Canvas Not Rendering

**Problem**: Video feed is blank

**Solutions**:
1. Open browser console (F12) for errors
2. Check canvas dimensions are set
3. Verify tracks data structure matches types
4. Try refreshing the page

### Performance Issues

**Problem**: Low FPS or laggy interface

**Solutions**:
1. Disable trajectories (press `T`)
2. Reduce track history in backend config
3. Check network latency
4. Use Chrome/Edge for better Canvas performance
5. Close other browser tabs

## 📊 Performance Metrics

### Expected Performance

| Metric | Target | Typical |
|--------|--------|---------|
| Frontend FPS | 60 | 55-60 |
| WebSocket Latency | <50ms | 20-40ms |
| Track Update Rate | 30 Hz | 28-30 Hz |
| Memory Usage | <200MB | 150MB |

### Monitoring

Open browser DevTools (F12):
- **Console**: WebSocket messages, errors
- **Network**: API calls, WebSocket traffic
- **Performance**: Frame rate, memory usage

## 🚢 Production Deployment

### Build for Production

```bash
cd frontend
npm run build

# Output in frontend/dist/
```

### Deploy with Docker

```bash
# Build and run
docker-compose up -d

# Check status
docker ps

# View logs
docker logs daemon-vision-frontend
```

### Deploy to Cloud

#### AWS S3 + CloudFront

```bash
# Build
npm run build

# Upload to S3
aws s3 sync dist/ s3://your-bucket/

# Invalidate CloudFront
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

#### Nginx

```bash
# Build
npm run build

# Copy to nginx
sudo cp -r dist/* /var/www/html/

# Restart nginx
sudo systemctl restart nginx
```

## 🔐 Security Considerations

### Production Checklist

- [ ] Enable HTTPS/WSS
- [ ] Add authentication (JWT tokens)
- [ ] Configure CORS properly
- [ ] Rate limit API endpoints
- [ ] Sanitize user inputs
- [ ] Enable CSP headers
- [ ] Use environment variables for secrets

### CORS Configuration

Backend `config.yaml`:

```yaml
api:
  cors_origins: 
    - "https://yourdomain.com"
    - "https://www.yourdomain.com"
```

## 📱 Mobile Support

The interface is optimized for desktop but has basic mobile support:

- Responsive layout
- Touch-friendly buttons
- Simplified metrics on small screens

For full mobile experience, consider:
- Dedicated mobile app
- Progressive Web App (PWA)
- Simplified mobile UI

## 🔄 Updates & Maintenance

### Updating Dependencies

```bash
cd frontend

# Check for updates
npm outdated

# Update all
npm update

# Update specific package
npm install react@latest
```

### Version Control

```bash
# Current version
cat package.json | grep version

# Update version
npm version patch  # 1.0.0 -> 1.0.1
npm version minor  # 1.0.0 -> 1.1.0
npm version major  # 1.0.0 -> 2.0.0
```

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [TailwindCSS Docs](https://tailwindcss.com/docs)
- [Canvas API Reference](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)

## 🆘 Support

For issues or questions:
1. Check this guide
2. Review backend logs
3. Check browser console
4. Contact Core team

---

**Built with precision. Deployed with confidence.**

PT. Daemon Blockint Technologies
