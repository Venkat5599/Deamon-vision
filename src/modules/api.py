"""
Module 5: Integration Interface
FastAPI REST endpoints and WebSocket for real-time track streaming.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional, Set
from datetime import datetime
import asyncio
import json
import logging
import os
import shutil

from ..core.models import (
    TrackObject, TrackListResponse, LockResponse,
    TrajectoryResponse, TrajectoryPoint
)

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection."""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection."""
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients."""
        if not self.active_connections:
            return
        
        message_json = json.dumps(message, default=str)
        
        # Send to all connections
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                logger.error(f"Error sending to WebSocket: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.disconnect(conn)


class DaemonVisionAPI:
    """FastAPI application for Daemon Vision."""
    
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8000,
        cors_origins: Optional[List[str]] = None
    ):
        """
        Initialize API.
        
        Args:
            host: Host address
            port: Port number
            cors_origins: Allowed CORS origins
        """
        self.host = host
        self.port = port
        self.cors_origins = cors_origins or ["*"]
        
        self.app = FastAPI(
            title="Daemon Vision API",
            description="Real-Time Multi-Target Detection, Tracking & Locking System",
            version="1.0.0"
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self.connection_manager = ConnectionManager()
        
        # Shared state (will be updated by pipeline)
        self.current_tracks: List[TrackObject] = []
        self.lock_manager = None  # Set by pipeline
        self.pipeline = None  # Set by pipeline for video source switching
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes."""
        
        @self.app.get("/")
        async def root():
            """Root endpoint."""
            return {
                "name": "Daemon Vision API",
                "version": "1.0.0",
                "status": "operational",
                "timestamp": datetime.now().isoformat()
            }
        
        @self.app.get("/health")
        async def health():
            """Health check endpoint."""
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "active_tracks": len(self.current_tracks),
                "websocket_connections": len(self.connection_manager.active_connections)
            }
        
        @self.app.get("/tracks", response_model=TrackListResponse)
        async def get_tracks():
            """Get all currently active tracks."""
            return TrackListResponse(
                tracks=self.current_tracks,
                timestamp=datetime.now()
            )
        
        @self.app.post("/lock/{track_id}", response_model=LockResponse)
        async def lock_target(track_id: int):
            """Lock onto a specific target by track ID."""
            if self.lock_manager is None:
                raise HTTPException(status_code=500, detail="Lock manager not initialized")
            
            # Attempt to lock
            success = self.lock_manager.lock_target(track_id, self.current_tracks)
            
            if not success:
                raise HTTPException(status_code=404, detail=f"Track {track_id} not found")
            
            # Find locked track
            locked_track = None
            for track in self.current_tracks:
                if track.track_id == track_id:
                    locked_track = track
                    break
            
            # Compute gimbal command
            gimbal_delta = None
            if locked_track:
                gimbal_delta = self.lock_manager.compute_gimbal_command(locked_track)
            
            return LockResponse(
                track_id=track_id,
                locked=True,
                gimbal_delta=gimbal_delta,
                timestamp=datetime.now()
            )
        
        @self.app.delete("/lock")
        async def unlock_target():
            """Release current lock."""
            if self.lock_manager is None:
                raise HTTPException(status_code=500, detail="Lock manager not initialized")
            
            self.lock_manager.unlock_target()
            
            return {
                "locked": False,
                "timestamp": datetime.now().isoformat()
            }
        
        @self.app.get("/lock/status")
        async def get_lock_status():
            """Get current lock status."""
            if self.lock_manager is None:
                raise HTTPException(status_code=500, detail="Lock manager not initialized")
            
            status = self.lock_manager.get_lock_status()
            status['timestamp'] = datetime.now().isoformat()
            return status
        
        @self.app.post("/upload/video")
        async def upload_video(file: UploadFile = File(...)):
            """Upload a video file for processing."""
            try:
                # Validate file type
                allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv']
                file_ext = os.path.splitext(file.filename)[1].lower()
                
                if file_ext not in allowed_extensions:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
                    )
                
                # Save uploaded file
                upload_path = os.path.join("data", "uploaded_video" + file_ext)
                os.makedirs("data", exist_ok=True)
                
                with open(upload_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                logger.info(f"Video uploaded: {upload_path}")
                
                # Switch video source if pipeline is available
                if self.pipeline:
                    await self.pipeline.switch_video_source(upload_path)
                    return {
                        "status": "success",
                        "message": "Video uploaded and processing started",
                        "filename": file.filename,
                        "path": upload_path,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "status": "success",
                        "message": "Video uploaded. Restart backend to process.",
                        "filename": file.filename,
                        "path": upload_path,
                        "timestamp": datetime.now().isoformat()
                    }
            
            except Exception as e:
                logger.error(f"Upload error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/track/{track_id}/trajectory", response_model=TrajectoryResponse)
        async def get_trajectory(track_id: int):
            """Get trajectory history for a specific track."""
            # Find track
            target_track = None
            for track in self.current_tracks:
                if track.track_id == track_id:
                    target_track = track
                    break
            
            if target_track is None:
                raise HTTPException(status_code=404, detail=f"Track {track_id} not found")
            
            return TrajectoryResponse(
                track_id=track_id,
                trajectory=target_track.trajectory,
                predicted_position=None,  # Placeholder for AI module
                velocity=target_track.velocity
            )
        
        @self.app.websocket("/stream")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time track updates."""
            await self.connection_manager.connect(websocket)
            
            try:
                # Send initial state
                await websocket.send_json({
                    "type": "connected",
                    "message": "Connected to Daemon Vision stream",
                    "timestamp": datetime.now().isoformat()
                })
                
                # Keep connection alive and handle incoming messages
                while True:
                    try:
                        # Wait for client messages (heartbeat, etc.)
                        data = await asyncio.wait_for(
                            websocket.receive_text(),
                            timeout=30.0
                        )
                        
                        # Echo heartbeat
                        if data == "ping":
                            await websocket.send_text("pong")
                    
                    except asyncio.TimeoutError:
                        # Send heartbeat
                        await websocket.send_json({
                            "type": "heartbeat",
                            "timestamp": datetime.now().isoformat()
                        })
            
            except WebSocketDisconnect:
                self.connection_manager.disconnect(websocket)
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                self.connection_manager.disconnect(websocket)
    
    async def broadcast_tracks(self, tracks: List[TrackObject], frame=None):
        """
        Broadcast track updates to all WebSocket clients.
        
        Args:
            tracks: Current tracks to broadcast
            frame: Optional video frame (numpy array)
        """
        self.current_tracks = tracks
        
        if not self.connection_manager.active_connections:
            return
        
        # Prepare message
        message = {
            "type": "track_update",
            "tracks": [track.dict() for track in tracks],
            "timestamp": datetime.now().isoformat()
        }
        
        # Add frame if provided (original resolution, maximum quality)
        if frame is not None:
            import cv2
            import base64
            
            # NO RESIZING - Keep original 1920x1080 resolution
            # Maximum quality JPEG compression
            _, buffer = cv2.imencode('.jpg', frame, [
                cv2.IMWRITE_JPEG_QUALITY, 95  # Maximum quality
            ])
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            message["frame"] = frame_base64
        
        await self.connection_manager.broadcast(message)
    
    def set_lock_manager(self, lock_manager):
        """Set lock manager reference."""
        self.lock_manager = lock_manager
    
    def set_pipeline(self, pipeline):
        """Set pipeline reference for video source switching."""
        self.pipeline = pipeline
