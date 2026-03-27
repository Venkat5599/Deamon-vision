import type { Track, BoundingBox } from '../types';

export class CanvasRenderer {
  private ctx: CanvasRenderingContext2D;
  private width: number;
  private height: number;

  constructor(canvas: HTMLCanvasElement) {
    const ctx = canvas.getContext('2d');
    if (!ctx) throw new Error('Failed to get canvas context');
    
    this.ctx = ctx;
    this.width = canvas.width;
    this.height = canvas.height;
  }

  clear() {
    this.ctx.clearRect(0, 0, this.width, this.height);
  }

  drawCrosshair() {
    const centerX = this.width / 2;
    const centerY = this.height / 2;
    const radius = 40;

    this.ctx.strokeStyle = '#000000';
    this.ctx.lineWidth = 0.5;
    this.ctx.globalAlpha = 0.3;

    // Circle
    this.ctx.beginPath();
    this.ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    this.ctx.stroke();

    // Crosshair lines
    this.ctx.lineWidth = 1;
    this.ctx.beginPath();
    this.ctx.moveTo(centerX - 20, centerY);
    this.ctx.lineTo(centerX + 20, centerY);
    this.ctx.moveTo(centerX, centerY - 20);
    this.ctx.lineTo(centerX, centerY + 20);
    this.ctx.stroke();

    this.ctx.globalAlpha = 1;
  }

  drawBoundingBox(bbox: BoundingBox, label: string, color: string = '#000000', isLocked: boolean = false) {
    const { x, y, w, h } = bbox;

    // Box
    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = isLocked ? 2 : 1.5;
    this.ctx.fillStyle = `${color}0D`; // 5% opacity
    this.ctx.fillRect(x, y, w, h);
    this.ctx.strokeRect(x, y, w, h);

    // Label
    this.ctx.font = '10px JetBrains Mono';
    this.ctx.fillStyle = color;
    this.ctx.fillText(label, x, y - 5);
  }

  drawTrajectory(points: Array<{ x: number; y: number }>, color: string = '#000000') {
    if (points.length < 2) return;

    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = 1;
    this.ctx.setLineDash([2, 2]);
    this.ctx.globalAlpha = 0.6;

    this.ctx.beginPath();
    this.ctx.moveTo(points[0].x, points[0].y);
    
    for (let i = 1; i < points.length; i++) {
      this.ctx.lineTo(points[i].x, points[i].y);
    }
    
    this.ctx.stroke();
    this.ctx.setLineDash([]);
    this.ctx.globalAlpha = 1;
  }

  drawCorners() {
    const cornerSize = 32;
    const margin = 16;

    this.ctx.strokeStyle = '#000000';
    this.ctx.lineWidth = 2;
    this.ctx.globalAlpha = 0.3;

    // Top-left
    this.ctx.beginPath();
    this.ctx.moveTo(margin + cornerSize, margin);
    this.ctx.lineTo(margin, margin);
    this.ctx.lineTo(margin, margin + cornerSize);
    this.ctx.stroke();

    // Top-right
    this.ctx.beginPath();
    this.ctx.moveTo(this.width - margin - cornerSize, margin);
    this.ctx.lineTo(this.width - margin, margin);
    this.ctx.lineTo(this.width - margin, margin + cornerSize);
    this.ctx.stroke();

    // Bottom-left
    this.ctx.beginPath();
    this.ctx.moveTo(margin, this.height - margin - cornerSize);
    this.ctx.lineTo(margin, this.height - margin);
    this.ctx.lineTo(margin + cornerSize, this.height - margin);
    this.ctx.stroke();

    // Bottom-right
    this.ctx.beginPath();
    this.ctx.moveTo(this.width - margin - cornerSize, this.height - margin);
    this.ctx.lineTo(this.width - margin, this.height - margin);
    this.ctx.lineTo(this.width - margin, this.height - margin - cornerSize);
    this.ctx.stroke();

    this.ctx.globalAlpha = 1;
  }

  drawTracks(tracks: Track[], showTrajectories: boolean = true) {
    tracks.forEach(track => {
      const color = track.is_locked ? '#000000' : 
                    track.confidence < 0.5 ? '#666666' : '#1a1a1a';
      
      const label = `TARGET_${String(track.track_id).padStart(2, '0')} [${track.class_name.toUpperCase()}] ${(track.confidence * 100).toFixed(0)}%`;
      
      this.drawBoundingBox(track.bbox, label, color, track.is_locked);
      
      if (showTrajectories && track.trajectory.length > 1) {
        this.drawTrajectory(track.trajectory, color);
      }
    });
  }

  render(tracks: Track[], showTrajectories: boolean = true) {
    this.clear();
    this.drawCrosshair();
    this.drawTracks(tracks, showTrajectories);
    this.drawCorners();
  }
}

// Export a simple function for direct use
export function drawTracks(
  ctx: CanvasRenderingContext2D,
  tracks: Track[],
  showTrajectories: boolean = true
) {
  tracks.forEach(track => {
    const color = track.is_locked ? '#000000' : 
                  track.confidence < 0.5 ? '#666666' : '#1a1a1a';
    
    const { x, y, w, h } = track.bbox;
    
    // Draw bounding box
    ctx.strokeStyle = color;
    ctx.lineWidth = track.is_locked ? 3 : 2;
    ctx.fillStyle = `${color}08`; // 3% opacity
    ctx.fillRect(x, y, w, h);
    ctx.strokeRect(x, y, w, h);
    
    // Draw label
    const label = `#${track.track_id} ${track.class_name} ${(track.confidence * 100).toFixed(0)}%`;
    ctx.font = 'bold 12px monospace';
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(x, y - 20, ctx.measureText(label).width + 8, 18);
    ctx.fillStyle = color;
    ctx.fillText(label, x + 4, y - 6);
    
    // Draw trajectory
    if (showTrajectories && track.trajectory.length > 1) {
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 5]);
      ctx.globalAlpha = 0.5;
      
      ctx.beginPath();
      ctx.moveTo(track.trajectory[0].x, track.trajectory[0].y);
      
      for (let i = 1; i < track.trajectory.length; i++) {
        ctx.lineTo(track.trajectory[i].x, track.trajectory[i].y);
      }
      
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.globalAlpha = 1;
    }
  });
}
