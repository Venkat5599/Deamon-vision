import { useEffect, useRef } from 'react';
import { Eye, EyeOff, Maximize2 } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { drawTracks } from '../utils/canvas';
import type { Track } from '../types';

interface VideoFeedProps {
  tracks: Track[];
  showTrajectories: boolean;
  onCanvasClick: (x: number, y: number) => void;
  onToggleTrajectories?: () => void;
  currentFrame?: string | null;
}

export function VideoFeed({ 
  tracks, 
  showTrajectories, 
  onCanvasClick,
  onToggleTrajectories,
  currentFrame
}: VideoFeedProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Resize canvas to fit container while maintaining aspect ratio
  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const resizeCanvas = () => {
      const containerWidth = container.clientWidth;
      const containerHeight = container.clientHeight;
      const videoAspectRatio = 16 / 9; // 1920x1080

      let canvasWidth = containerWidth;
      let canvasHeight = containerWidth / videoAspectRatio;

      if (canvasHeight > containerHeight) {
        canvasHeight = containerHeight;
        canvasWidth = containerHeight * videoAspectRatio;
      }

      canvas.style.width = `${canvasWidth}px`;
      canvas.style.height = `${canvasHeight}px`;
    };

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    return () => window.removeEventListener('resize', resizeCanvas);
  }, []);

  // Draw frame and tracks
  useEffect(() => {
    const canvas = canvasRef.current;
    const img = imageRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Draw video frame if available
    if (currentFrame && img) {
      img.onload = () => {
        // Set canvas internal resolution to match image
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        
        // Clear and draw the image at original size
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        
        // Draw tracks on top
        drawTracks(ctx, tracks, showTrajectories);
      };
      img.src = currentFrame;
    } else {
      // Draw grid background if no frame
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.strokeStyle = 'rgba(0, 230, 57, 0.05)';
      ctx.lineWidth = 1;
      const gridSize = 40;
      
      for (let x = 0; x < canvas.width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
      }
      
      for (let y = 0; y < canvas.height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
      }

      // Draw tracks only
      drawTracks(ctx, tracks, showTrajectories);
    }
  }, [tracks, showTrajectories, currentFrame]);

  const handleClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * canvas.width;
    const y = ((e.clientY - rect.top) / rect.height) * canvas.height;

    onCanvasClick(x, y);
  };

  return (
    <Card className="flex-1 overflow-hidden bg-black/50 backdrop-blur">
      <CardContent ref={containerRef} className="p-0 h-full relative flex items-center justify-center">
        {/* Controls Overlay */}
        <div className="absolute top-4 right-4 z-10 flex gap-2">
          <Button
            size="icon"
            variant="secondary"
            onClick={onToggleTrajectories}
            className="bg-background/80 backdrop-blur hover:bg-background/90"
            title={showTrajectories ? "Hide Trajectories (T)" : "Show Trajectories (T)"}
          >
            {showTrajectories ? (
              <Eye className="h-4 w-4" />
            ) : (
              <EyeOff className="h-4 w-4" />
            )}
          </Button>
          <Button
            size="icon"
            variant="secondary"
            className="bg-background/80 backdrop-blur hover:bg-background/90"
            title="Fullscreen"
          >
            <Maximize2 className="h-4 w-4" />
          </Button>
        </div>

        {/* Status Overlay */}
        <div className="absolute top-4 left-4 z-10 bg-background/80 backdrop-blur px-3 py-2 rounded-lg border border-border/50">
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-red-500 animate-pulse-glow" />
            <span className="text-xs font-mono text-muted-foreground">
              REC {new Date().toLocaleTimeString()}
            </span>
          </div>
        </div>

        {/* Hidden image for loading frames */}
        <img ref={imageRef} className="hidden" alt="" />

        {/* Canvas - properly sized to maintain aspect ratio */}
        <canvas
          ref={canvasRef}
          width={1920}
          height={1080}
          onClick={handleClick}
          className="cursor-crosshair scanline"
          style={{ 
            imageRendering: 'auto',
            display: 'block'
          }}
        />

        {/* No Feed Overlay */}
        {tracks.length === 0 && !currentFrame && (
          <div className="absolute inset-0 flex items-center justify-center bg-background/50 backdrop-blur-sm">
            <div className="text-center space-y-4 max-w-md px-6">
              <div className="h-20 w-20 mx-auto rounded-full bg-primary/10 flex items-center justify-center">
                <Eye className="h-10 w-10 text-primary/50" />
              </div>
              <div className="space-y-2">
                <p className="text-lg font-semibold text-foreground">
                  No Video Feed
                </p>
                <p className="text-sm text-muted-foreground">
                  Click the "Upload Video" button in the header to select a video file
                </p>
              </div>
              <div className="pt-2 text-xs text-muted-foreground/70 space-y-1">
                <p>Supported formats: MP4, AVI, MOV, MKV</p>
                <p>Best content: Traffic, pedestrians, parking lots</p>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
