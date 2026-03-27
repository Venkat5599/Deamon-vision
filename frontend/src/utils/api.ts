import type { Track, LockResponse, TrackListResponse } from '../types';

const API_BASE = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';

export class DaemonVisionAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE) {
    this.baseUrl = baseUrl;
  }

  async getTracks(): Promise<Track[]> {
    const response = await fetch(`${this.baseUrl}/tracks`);
    if (!response.ok) throw new Error('Failed to fetch tracks');
    const data: TrackListResponse = await response.json();
    return data.tracks;
  }

  async lockTarget(trackId: number): Promise<LockResponse> {
    const response = await fetch(`${this.baseUrl}/lock/${trackId}`, {
      method: 'POST'
    });
    if (!response.ok) throw new Error(`Failed to lock track ${trackId}`);
    return response.json();
  }

  async unlockTarget(): Promise<void> {
    const response = await fetch(`${this.baseUrl}/lock`, {
      method: 'DELETE'
    });
    if (!response.ok) throw new Error('Failed to unlock target');
  }

  async getLockStatus(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/lock/status`);
    if (!response.ok) throw new Error('Failed to get lock status');
    return response.json();
  }

  async getTrajectory(trackId: number): Promise<any> {
    const response = await fetch(`${this.baseUrl}/track/${trackId}/trajectory`);
    if (!response.ok) throw new Error(`Failed to get trajectory for track ${trackId}`);
    return response.json();
  }

  async getHealth(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) throw new Error('Failed to get health status');
    return response.json();
  }

  async uploadVideo(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/upload/video`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to upload video');
    }

    return response.json();
  }

  createWebSocket(): WebSocket {
    const wsUrl = this.baseUrl.replace('http', 'ws');
    return new WebSocket(`${wsUrl}/stream`);
  }
}

export const api = new DaemonVisionAPI();
