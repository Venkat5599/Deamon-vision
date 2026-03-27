import { useRef } from 'react';
import { Upload, Activity, Wifi, WifiOff, Video } from 'lucide-react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { cn } from '../lib/utils';

interface HeaderProps {
  isConnected: boolean;
  fps: number;
  latency: number;
  onVideoUpload?: (file: File) => void;
}

export function Header({ isConnected, fps, latency, onVideoUpload }: HeaderProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && onVideoUpload) {
      onVideoUpload(file);
      // Reset input so same file can be selected again
      e.target.value = '';
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-6">
        {/* Logo and Title */}
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3">
            <div className="relative">
              <Activity className="h-8 w-8 text-primary" strokeWidth={2.5} />
              <div className={cn(
                "absolute -right-1 -top-1 h-3 w-3 rounded-full",
                isConnected ? "bg-primary animate-pulse-glow" : "bg-destructive"
              )} />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-primary glow-text">
                DAEMON VISION
              </h1>
              <p className="text-xs text-muted-foreground font-mono">
                Multi-Target Tracking System
              </p>
            </div>
          </div>
        </div>

        {/* Status and Actions */}
        <div className="flex items-center gap-4">
          {/* Metrics */}
          <div className="hidden md:flex items-center gap-4 px-4 py-2 rounded-lg bg-card border border-border/50">
            <div className="flex flex-col items-end">
              <span className="text-xs text-muted-foreground font-mono">FPS</span>
              <span className="text-sm font-bold font-mono text-primary">{fps.toFixed(1)}</span>
            </div>
            <div className="h-8 w-px bg-border" />
            <div className="flex flex-col items-end">
              <span className="text-xs text-muted-foreground font-mono">LATENCY</span>
              <span className="text-sm font-bold font-mono text-primary">{latency.toFixed(0)}ms</span>
            </div>
          </div>

          {/* Connection Status */}
          <Badge 
            variant={isConnected ? "default" : "destructive"}
            className="gap-1.5 px-3 py-1.5"
          >
            {isConnected ? (
              <>
                <Wifi className="h-3 w-3" />
                <span className="font-mono text-xs">ONLINE</span>
              </>
            ) : (
              <>
                <WifiOff className="h-3 w-3" />
                <span className="font-mono text-xs">OFFLINE</span>
              </>
            )}
          </Badge>

          {/* Upload Button */}
          <Button 
            variant="outline" 
            size="sm" 
            className="gap-2"
            onClick={handleUploadClick}
            title="Click to select video file (MP4, AVI, MOV, MKV)"
          >
            <Video className="h-4 w-4" />
            <span className="hidden sm:inline">Upload Video</span>
            <Upload className="h-3 w-3 opacity-70" />
          </Button>

          {/* Hidden File Input */}
          <input
            ref={fileInputRef}
            type="file"
            accept="video/mp4,video/avi,video/mov,video/mkv,video/*"
            onChange={handleFileChange}
            className="hidden"
            aria-label="Upload video file"
          />
        </div>
      </div>
    </header>
  );
}
