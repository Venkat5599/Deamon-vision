import { Target, AlertCircle } from 'lucide-react';
import { TrackCard } from './TrackCard';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import type { Track } from '../types';

interface TrackListProps {
  tracks: Track[];
  onLock: (trackId: number) => void;
}

export function TrackList({ tracks, onLock }: TrackListProps) {
  const lockedTrack = tracks.find(t => t.is_locked);
  const activeTracks = tracks.filter(t => !t.is_locked);

  return (
    <aside className="w-80 flex flex-col gap-4 overflow-hidden">
      {/* Locked Target */}
      {lockedTrack && (
        <Card className="border-primary/50 bg-primary/5">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm flex items-center gap-2 text-primary">
              <Target className="h-4 w-4" />
              Locked Target
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <TrackCard track={lockedTrack} onLock={onLock} />
          </CardContent>
        </Card>
      )}

      {/* Active Tracks */}
      <Card className="flex-1 flex flex-col overflow-hidden">
        <CardHeader className="pb-3">
          <CardTitle className="text-sm flex items-center justify-between">
            <span className="flex items-center gap-2">
              <Target className="h-4 w-4" />
              Active Tracks
            </span>
            <span className="text-xs font-mono text-muted-foreground">
              {activeTracks.length} detected
            </span>
          </CardTitle>
        </CardHeader>
        <CardContent className="flex-1 overflow-y-auto pt-0 space-y-3">
          {activeTracks.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center p-6">
              <AlertCircle className="h-12 w-12 text-muted-foreground/50 mb-3" />
              <p className="text-sm text-muted-foreground">
                No active tracks detected
              </p>
              <p className="text-xs text-muted-foreground/70 mt-1">
                Waiting for objects to appear...
              </p>
            </div>
          ) : (
            activeTracks.map((track) => (
              <TrackCard key={track.track_id} track={track} onLock={onLock} />
            ))
          )}
        </CardContent>
      </Card>
    </aside>
  );
}
