import { Activity, Clock, Target, Zap } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import type { Track } from '../types';

interface MetricsDashboardProps {
  tracks: Track[];
  fps: number;
  latency: number;
}

export function MetricsDashboard({ tracks, latency }: MetricsDashboardProps) {
  const lockedCount = tracks.filter(t => t.is_locked).length;
  const avgConfidence = tracks.length > 0
    ? tracks.reduce((sum, t) => sum + t.confidence, 0) / tracks.length
    : 0;

  const metrics = [
    {
      label: 'Active Tracks',
      value: tracks.length,
      icon: Target,
      color: 'text-blue-400',
    },
    {
      label: 'Locked Targets',
      value: lockedCount,
      icon: Activity,
      color: 'text-primary',
    },
    {
      label: 'Avg Confidence',
      value: `${(avgConfidence * 100).toFixed(1)}%`,
      icon: Zap,
      color: 'text-yellow-400',
    },
    {
      label: 'Processing Time',
      value: `${latency.toFixed(0)}ms`,
      icon: Clock,
      color: 'text-purple-400',
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {metrics.map((metric) => (
        <Card key={metric.label} className="bg-card/50 backdrop-blur">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <p className="text-xs text-muted-foreground font-medium">
                  {metric.label}
                </p>
                <p className="text-2xl font-bold font-mono">
                  {metric.value}
                </p>
              </div>
              <metric.icon className={`h-8 w-8 ${metric.color} opacity-80`} />
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
