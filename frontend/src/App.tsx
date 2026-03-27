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
  const { tracks, isConnected, currentFrame, fps: wsFps, latency: wsLatency } = useWebSocket();
  const [showTrajectories, setShowTrajectories] = useState(true);
  const [fps, setFps] = useState(0);
  const [latency, setLatency] = useState(0);

  // Use WebSocket metrics when available
  useEffect(() => {
    if (wsFps > 0) {
      setFps(wsFps);
    }
    if (wsLatency > 0) {
      setLatency(wsLatency);
    }
  }, [wsFps, wsLatency]);

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
      
      // Check if track exists before trying to lock
      if (!lockedTrack) {
        toast.error(`Track #${trackId} is no longer visible`);
        return;
      }
      
      if (lockedTrack.is_locked) {
        await api.unlockTarget();
        toast.success('Target unlocked');
      } else {
        try {
          await api.lockTarget(trackId);
          toast.success(`🎯 Locked onto ${lockedTrack.class_name} #${trackId}`);
        } catch (lockError: any) {
          // Track disappeared between check and lock
          toast.warning(`Track #${trackId} moved out of frame. Try again.`);
        }
      }
    } catch (error: any) {
      console.error('Failed to lock/unlock target:', error);
      toast.error('Lock operation failed');
    }
  }, [tracks]);

  const handleCanvasClick = useCallback((x: number, y: number) => {
    if (tracks.length === 0) {
      toast.info('No active tracks to lock');
      return;
    }
    
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
    } else {
      toast.info('Click closer to a tracked object');
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
        } else {
          toast.info(`Track #${trackId} not found. Check Active Tracks sidebar.`);
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
              <span className={isConnected ? 'text-foreground font-semibold' : 'text-muted-foreground'}>
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
