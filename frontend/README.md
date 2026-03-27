# Daemon Vision - Frontend

Real-time surveillance operator interface for Daemon Vision multi-target tracking system.

## Features

- Real-time WebSocket connection to backend
- Live video feed with tactical overlay
- Track visualization with bounding boxes and trajectories
- Interactive track locking/unlocking
- Performance metrics dashboard
- Keyboard shortcuts for quick operations
- Military-grade tactical UI design

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Daemon Vision backend running on `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
# Start development server
npm run dev

# Open browser to http://localhost:3000
```

### Build for Production

```bash
npm run build
npm run preview
```

## Keyboard Shortcuts

- `T` - Toggle trajectory display
- `U` - Unlock current target
- `1-9` - Lock track by ID
- Click on canvas - Lock nearest track

## Configuration

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

## Architecture

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.tsx          # Top navigation bar
│   │   ├── VideoFeed.tsx       # Canvas overlay for tracks
│   │   ├── TrackList.tsx       # Track list panel
│   │   ├── TrackCard.tsx       # Individual track card
│   │   └── MetricsDashboard.tsx # Performance metrics
│   ├── hooks/
│   │   └── useWebSocket.ts     # WebSocket connection hook
│   ├── utils/
│   │   ├── api.ts              # REST API client
│   │   └── canvas.ts           # Canvas rendering utilities
│   ├── types/
│   │   └── index.ts            # TypeScript interfaces
│   ├── App.tsx                 # Main application
│   └── main.tsx                # Entry point
├── package.json
├── vite.config.ts
└── tailwind.config.js
```

## API Integration

The frontend connects to the Daemon Vision backend API:

- `GET /tracks` - Fetch all active tracks
- `POST /lock/{track_id}` - Lock onto target
- `DELETE /lock` - Unlock target
- `GET /health` - System health check
- `WS /stream` - Real-time track updates

## Tech Stack

- React 18 with TypeScript
- Vite for build tooling
- TailwindCSS for styling
- Canvas API for video overlay
- WebSocket for real-time updates
- Recharts for metrics visualization

## Development

### Project Structure

- `components/` - React components
- `hooks/` - Custom React hooks
- `utils/` - Utility functions
- `types/` - TypeScript type definitions

### Adding New Features

1. Define types in `src/types/index.ts`
2. Create component in `src/components/`
3. Add API methods in `src/utils/api.ts`
4. Integrate in `src/App.tsx`

## Troubleshooting

### WebSocket Connection Failed

- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in backend
- Verify WebSocket endpoint is accessible

### Canvas Not Rendering

- Check browser console for errors
- Ensure tracks data is being received
- Verify canvas dimensions are set correctly

### Performance Issues

- Reduce trajectory history length
- Disable trajectory rendering
- Check network latency

## License

Confidential - PT. Daemon Blockint Technologies
