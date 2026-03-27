import { Lock, Unlock, TrendingUp, MapPin } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { cn } from '../lib/utils';
import type { Track } from '../types';

interface TrackCardProps {
  track: Track;
  onLock: (trackId: number) => void;
}

export function TrackCard({ track, onLock }: TrackCardProps) {
  const getClassColor = (className: string) => {
    const colors: Record<string, string> = {
      person: 'text-blue-400',
      car: 'text-yellow-400',
      truck: 'text-orange-400',
      bus: 'text-purple-400',
      motorcycle: 'text-pink-400',
      bicycle: 'text-green-400',
      airplane: 'text-cyan-400',
    };
    return colors[className] || 'text-gray-400';
  };

  return (
    <Card className={cn(
      "transition-all duration-200 hover:shadow-lg hover:shadow-primary/20",
      track.is_locked && "ring-2 ring-primary shadow-lg shadow-primary/30"
    )}>
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-2">
            <Badge variant={track.is_locked ? "default" : "secondary"} className="font-mono">
              ID {track.track_id}
            </Badge>
            <span className={cn("text-sm font-medium capitalize", getClassColor(track.class_name))}>
              {track.class_name}
            </span>
          </div>
          <Button
            size="icon"
            variant={track.is_locked ? "default" : "outline"}
            onClick={() => onLock(track.track_id)}
            className="h-8 w-8"
          >
            {track.is_locked ? (
              <Lock className="h-4 w-4" />
            ) : (
              <Unlock className="h-4 w-4" />
            )}
          </Button>
        </div>

        <div className="space-y-2 text-xs">
          <div className="flex items-center justify-between">
            <span className="text-muted-foreground flex items-center gap-1">
              <TrendingUp className="h-3 w-3" />
              Confidence
            </span>
            <span className="font-mono font-medium">
              {(track.confidence * 100).toFixed(1)}%
            </span>
          </div>

          {track.velocity && (
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">Velocity</span>
              <span className="font-mono font-medium">
                {Math.sqrt(track.velocity.vx ** 2 + track.velocity.vy ** 2).toFixed(2)} m/s
              </span>
            </div>
          )}

          {track.ground_coord && (
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground flex items-center gap-1">
                <MapPin className="h-3 w-3" />
                Position
              </span>
              <span className="font-mono text-[10px]">
                {track.ground_coord.lat.toFixed(4)}, {track.ground_coord.lon.toFixed(4)}
              </span>
            </div>
          )}

          <div className="flex items-center justify-between pt-2 border-t border-border/50">
            <span className="text-muted-foreground">Frames</span>
            <span className="font-mono font-medium">
              {track.frames_since_update}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
