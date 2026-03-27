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
      color: 'text-gray-700',
    },
    {
      label: 'Locked Targets',
      value: lockedCount,
      icon: Activity,
      color: 'text-foreground',
    },
    {
      label: 'Avg Confidence',
      value: `${(avgConfidence * 100).toFixed(1)}%`,
      icon: Zap,
      color: 'text-gray-600',
    },
    {
      label: 'Processing Time',
      value: `${latency.toFixed(0)}ms`,
      icon: Clock,
      color: 'text-gray-700',
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {metrics.map((metric) => (
        <Card key={metric.label} className="bg-card backdrop-blur">
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
              <metric.icon className={`h-8 w-8 ${metric.color}`} />
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
