"""
Demo script for Daemon Vision with visualization.
Shows detection, tracking, and locking in real-time.
"""
import asyncio
import cv2
import numpy as np
from datetime import datetime
import argparse
from pathlib import Path

from src.modules.sensor_ingestion import SensorDataCollector
from src.modules.detection import ObjectDetector
from src.modules.tracking import ByteTracker
from src.modules.locking import TargetLockManager


class DaemonVisionDemo:
    """Demo visualization for Daemon Vision."""
    
    def __init__(self, video_path: str, device: str = "cuda"):
        self.video_path = video_path
        self.device = device
        
        self.sensor = None
        self.detector = None
        self.tracker = None
        self.lock_manager = None
        
        self.paused = False
        self.show_trajectories = True
        self.auto_lock_highest_priority = False
    
    async def initialize(self):
        """Initialize all components."""
        print("Initializing Daemon Vision Demo...")
        
        self.sensor = SensorDataCollector(
            video_source=self.video_path,
            fps=30,
            enable_stabilization=False,
            imgsz=640
        )
        await self.sensor.initialize()
        
        self.detector = ObjectDetector(
            model_path="yolov8n.pt",
            confidence_threshold=0.5,
            device=self.device,
            half_precision=(self.device == "cuda")
        )
        self.detector.initialize()
        
        self.tracker = ByteTracker()
        
        self.lock_manager = TargetLockManager(
            image_width=640,
            image_height=640
        )
        
        print("Initialization complete!")
    
    def draw_tracks(self, frame: np.ndarray, tracks: list) -> np.ndarray:
        """Draw tracks on frame."""
        output = frame.copy()
        
        for track in tracks:
            x1, y1, x2, y2 = track.bbox.to_xyxy()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Color based on lock status
            if track.is_locked:
                color = (0, 0, 255)  # Red for locked
                thickness = 3
            else:
                color = (0, 255, 0)  # Green for tracked
                thickness = 2
            
            # Draw bounding box
            cv2.rectangle(output, (x1, y1), (x2, y2), color, thickness)
            
            # Draw label
            label = f"ID:{track.track_id} {track.class_name.value} {track.confidence:.2f}"
            if track.velocity:
                label += f" v:{track.velocity.magnitude:.1f}"
            
            (label_w, label_h), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
            )
            cv2.rectangle(
                output,
                (x1, y1 - label_h - 10),
                (x1 + label_w, y1),
                color,
                -1
            )
            cv2.putText(
                output,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )
            
            # Draw trajectory
            if self.show_trajectories and len(track.trajectory) > 1:
                points = [(int(p.x), int(p.y)) for p in track.trajectory]
                for i in range(len(points) - 1):
                    cv2.line(output, points[i], points[i + 1], color, 1)
            
            # Draw center point
            center = track.bbox.center
            cv2.circle(output, (int(center[0]), int(center[1])), 3, color, -1)
        
        return output
    
    def draw_info(self, frame: np.ndarray, tracks: list, fps: float) -> np.ndarray:
        """Draw info overlay."""
        output = frame.copy()
        h, w = output.shape[:2]
        
        # Semi-transparent overlay
        overlay = output.copy()
        cv2.rectangle(overlay, (10, 10), (300, 150), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, output, 0.5, 0, output)
        
        # Info text
        info_lines = [
            f"FPS: {fps:.1f}",
            f"Active Tracks: {len(tracks)}",
            f"Total Tracks: {self.tracker.total_tracks}",
            f"Locked: {self.lock_manager.locked_track_id or 'None'}",
        ]
        
        y_offset = 30
        for line in info_lines:
            cv2.putText(
                output, line, (20, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1
            )
            y_offset += 25
        
        # Controls
        controls = [
            "Controls:",
            "SPACE - Pause/Resume",
            "T - Toggle Trajectories",
            "A - Auto-lock Highest Priority",
            "1-9 - Lock Track by ID",
            "U - Unlock",
            "Q - Quit"
        ]
        
        y_offset = h - 200
        for line in controls:
            cv2.putText(
                output, line, (20, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1
            )
            y_offset += 20
        
        return output
    
    async def run(self):
        """Run demo."""
        if not all([self.sensor, self.detector, self.tracker, self.lock_manager]):
            await self.initialize()
        
        print("\nStarting demo...")
        print("Controls:")
        print("  SPACE - Pause/Resume")
        print("  T - Toggle Trajectories")
        print("  A - Auto-lock Highest Priority")
        print("  1-9 - Lock Track by ID")
        print("  U - Unlock")
        print("  Q - Quit\n")
        
        cv2.namedWindow("Daemon Vision Demo", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Daemon Vision Demo", 1280, 720)
        
        frame_count = 0
        start_time = datetime.now()
        
        while True:
            if not self.paused:
                # Get frame
                frame_data = await self.sensor.get_frame()
                if frame_data is None:
                    print("End of video")
                    break
                
                frame, metadata = frame_data
                frame_count += 1
                
                # Detection
                detections = self.detector.detect(frame, metadata)
                
                # Tracking
                tracks = self.tracker.update(detections, metadata)
                
                # Auto-lock highest priority
                if self.auto_lock_highest_priority and tracks:
                    prioritized = self.lock_manager.prioritize_tracks(tracks)
                    if prioritized and self.lock_manager.locked_track_id is None:
                        self.lock_manager.lock_target(prioritized[0].track_id, tracks)
                
                # Update lock
                self.lock_manager.update_lock(tracks)
                
                # Calculate FPS
                elapsed = (datetime.now() - start_time).total_seconds()
                fps = frame_count / elapsed if elapsed > 0 else 0
                
                # Draw visualization
                vis_frame = self.draw_tracks(frame, tracks)
                vis_frame = self.draw_info(vis_frame, tracks, fps)
                
                # Display
                cv2.imshow("Daemon Vision Demo", vis_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord(' '):
                self.paused = not self.paused
                print(f"{'Paused' if self.paused else 'Resumed'}")
            elif key == ord('t'):
                self.show_trajectories = not self.show_trajectories
                print(f"Trajectories: {'ON' if self.show_trajectories else 'OFF'}")
            elif key == ord('a'):
                self.auto_lock_highest_priority = not self.auto_lock_highest_priority
                print(f"Auto-lock: {'ON' if self.auto_lock_highest_priority else 'OFF'}")
            elif key == ord('u'):
                self.lock_manager.unlock_target()
                print("Unlocked")
            elif ord('1') <= key <= ord('9'):
                track_id = key - ord('0')
                if self.lock_manager.lock_target(track_id, tracks):
                    print(f"Locked track {track_id}")
                else:
                    print(f"Track {track_id} not found")
        
        cv2.destroyAllWindows()
        await self.sensor.close()
        
        print(f"\nDemo complete. Processed {frame_count} frames.")


async def main():
    parser = argparse.ArgumentParser(description='Daemon Vision Demo')
    parser.add_argument('--video', type=str, required=True, help='Path to video file')
    parser.add_argument('--device', type=str, default='cuda', choices=['cuda', 'cpu'])
    
    args = parser.parse_args()
    
    if not Path(args.video).exists():
        print(f"Error: Video file not found: {args.video}")
        return
    
    demo = DaemonVisionDemo(args.video, args.device)
    await demo.run()


if __name__ == "__main__":
    asyncio.run(main())
