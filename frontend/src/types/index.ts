export interface BoundingBox {
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface GroundCoordinate {
  lat: number;
  lon: number;
  alt?: number;
}

export interface Velocity {
  vx: number;
  vy: number;
}

export interface TrajectoryPoint {
  x: number;
  y: number;
  timestamp: string;
}

export interface Track {
  track_id: number;
  class_name: string;
  confidence: number;
  bbox: BoundingBox;
  ground_coord?: GroundCoordinate;
  velocity?: Velocity;
  trajectory: TrajectoryPoint[];
  last_seen: string;
  frames_since_update: number;
  is_locked: boolean;
}

export interface GimbalCommand {
  azimuth: number;
  elevation: number;
}

export interface LockResponse {
  track_id: number;
  locked: boolean;
  gimbal_delta?: GimbalCommand;
  timestamp: string;
}

export interface TrackListResponse {
  tracks: Track[];
  timestamp: string;
}

export interface WebSocketMessage {
  type: 'track_update' | 'heartbeat' | 'connected';
  tracks?: Track[];
  timestamp: string;
  message?: string;
}

export interface SystemMetrics {
  fps: number;
  latency: number;
  activeConnections: number;
  activeTracks: number;
}
