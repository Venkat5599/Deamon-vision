import { useEffect, useRef, useState, useCallback } from 'react';
import type { WebSocketMessage, Track } from '../types';
import { api } from '../utils/api';

export function useWebSocket() {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [currentFrame, setCurrentFrame] = useState<string | null>(null);
  const [fps, setFps] = useState(0);
  const [latency, setLatency] = useState(0);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout>>();

  const connect = useCallback(() => {
    try {
      const ws = api.createWebSocket();
      
      ws.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          
          if (message.type === 'track_update' && message.tracks) {
            setTracks(message.tracks);
            setLastUpdate(new Date());
            
            // Update frame if provided
            if ((message as any).frame) {
              const frameData = `data:image/jpeg;base64,${(message as any).frame}`;
              setCurrentFrame(frameData);
              console.log('Frame received, size:', (message as any).frame.length);
            }
            
            // Update metrics if provided
            if ((message as any).metrics) {
              const metrics = (message as any).metrics;
              console.log('Metrics received:', metrics);
              if (metrics.fps !== undefined) {
                setFps(metrics.fps);
              }
              if (metrics.latency !== undefined) {
                setLatency(metrics.latency);
              }
            }
          } else if (message.type === 'connected') {
            console.log('Connected to Daemon Vision:', message.message);
          }
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);
        
        // Auto-reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          console.log('Attempting to reconnect...');
          connect();
        }, 3000);
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      setIsConnected(false);
    }
  }, []);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  const sendHeartbeat = useCallback(() => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send('ping');
    }
  }, []);

  useEffect(() => {
    connect();

    // Send heartbeat every 10 seconds
    const heartbeatInterval = setInterval(sendHeartbeat, 10000);

    return () => {
      clearInterval(heartbeatInterval);
      disconnect();
    };
  }, [connect, disconnect, sendHeartbeat]);

  return {
    tracks,
    isConnected,
    lastUpdate,
    currentFrame,
    fps,
    latency,
    reconnect: connect
  };
}
