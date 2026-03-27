import { useState, useEffect, useCallback } from 'react';
import { Toaster } from 'sonner';
import { toast } from 'sonner';
import { Header } from './components/Header';
import { VideoFeed } from './components/VideoFeed';
import { TrackList } from './components/TrackList';
import { MetricsDashboard } from './components/MetricsDashboard';
import { useWebSocket } from './hooks/useWebSocket';
import { api } from './utils/api';
import type { Track } from './types';

function App() {
  const { tracks, isConnected, lastUpdate, currentFrame } = useWebSocket();
  const [showTrajectories, setShowTrajectories] = useState(true);
  const [fps, setFps] = useState(0);
  const [latency, setLatency] = useState(0);

  // Calculate FPS from updates
  useEffect(() => {
    if (!lastUpdate) return;
    
    const interval = setInterval(() => {
      const now = new Date();
      const diff = now.getTime() - lastUpdate.getTime();
      const calculatedFps = diff > 0 ? 1000 / diff : 0;
      setFps(Math.min(calculatedFps, 120));
    }, 1000);

    return () => clearInterval(interval);
  }, [lastUpdate]);

  // Fetch health metrics
  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const health = await api.getHealth();
        // Update latency if available
        if (health.latency !== undefined) {
          setLatency(health.latency);
        }
      } catch (error) {
        console.error('Failed to fetch health:', error);
      }
    };

    const interval = setInterval(fetchHealth, 5000);
    fetchHealth();

    return () => clearInterval(interval);
  }, []);

  const handleVideoUpload = useCallback(async (file: File) => {
    const uploadPromise = api.uploadVideo(file);

    toast.promise(uploadPromise, {
      loading: `Uploading ${file.name}...`,
      success: (result) => {
        return result.message || 'Video uploaded successfully!';
      },
      error: (error) => {
        return `Upload failed: ${error.message}`;
      },
    });

    try {
      await uploadPromise;
    } catch (error) {
      console.error('Upload error:', error);
    }
  }, []);

  const handleLock = useCallback(async (trackId: number) => {
    try {
      const lockedTrack = tracks.find(t => t.track_id === trackId);
      if (lockedTrack?.is_locked) {
        await api.unlockTarget();
        toast.success('Target unlocked');
      } else {
        await api.lockTarget(trackId);
        toast.success(`Locked onto target #${trackId}`);
      }
    } catch (error) {
      console.error('Failed to lock/unlock target:', error);
      toast.error('Failed to lock target');
    }
  }, [tracks]);

  const handleCanvasClick = useCallback((x: number, y: number) => {
    if (tracks.length === 0) return;
    
    // Find nearest track to click position
    let nearestTrack: Track | undefined;
    let minDistance = Infinity;

    for (const track of tracks) {
      const centerX = track.bbox.x + track.bbox.w / 2;
      const centerY = track.bbox.y + track.bbox.h / 2;
      const distance = Math.sqrt((x - centerX) ** 2 + (y - centerY) ** 2);

      if (distance < minDistance && distance < 100) {
        minDistance = distance;
        nearestTrack = track;
      }
    }

    if (nearestTrack) {
      handleLock(nearestTrack.track_id);
    }
  }, [tracks, handleLock]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === 't' || e.key === 'T') {
        setShowTrajectories(prev => !prev);
        toast.info(`Trajectories ${!showTrajectories ? 'shown' : 'hidden'}`);
      } else if (e.key === 'u' || e.key === 'U') {
        api.unlockTarget()
          .then(() => toast.success('All targets unlocked'))
          .catch(console.error);
      } else if (e.key >= '1' && e.key <= '9') {
        const trackId = parseInt(e.key);
        const track = tracks.find(t => t.track_id === trackId);
        if (track) {
          handleLock(trackId);
        }
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [handleLock, showTrajectories, tracks]);

  return (
    <div className="min-h-screen bg-background text-foreground antialiased">
      <Toaster position="top-right" richColors />
      
      <Header 
        isConnected={isConnected} 
        fps={fps} 
        latency={latency}
        onVideoUpload={handleVideoUpload}
      />

      <main className="container mx-auto p-6 space-y-6">
        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-6 h-[calc(100vh-200px)]">
          {/* Video Feed */}
          <VideoFeed
            tracks={tracks}
            showTrajectories={showTrajectories}
            onCanvasClick={handleCanvasClick}
            onToggleTrajectories={() => setShowTrajectories(prev => !prev)}
            currentFrame={currentFrame}
          />

          {/* Track List */}
          <TrackList tracks={tracks} onLock={handleLock} />
        </div>

        {/* Metrics Dashboard */}
        <MetricsDashboard tracks={tracks} fps={fps} latency={latency} />
      </main>

      {/* Footer */}
      <footer className="border-t border-border/40 bg-card/50 backdrop-blur">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between text-xs text-muted-foreground font-mono">
            <div className="flex items-center gap-4">
              <span>DAEMON VISION v1.0.0</span>
              <span className="hidden sm:inline">•</span>
              <span className="hidden sm:inline">PT. Daemon Blockint Technologies</span>
            </div>
            <div className="flex items-center gap-4">
              <span>Tracks: {tracks.length}</span>
              <span>•</span>
              <span className={isConnected ? 'text-primary' : 'text-destructive'}>
                {isConnected ? 'CONNECTED' : 'DISCONNECTED'}
              </span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
