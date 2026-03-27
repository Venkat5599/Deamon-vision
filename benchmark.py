"""
Benchmark script for Daemon Vision pipeline.
Measures FPS, latency, and tracking metrics.
"""
import asyncio
import argparse
import time
import numpy as np
from datetime import datetime
from pathlib import Path

from src.modules.sensor_ingestion import SensorDataCollector
from src.modules.detection import ObjectDetector
from src.modules.tracking import ByteTracker


async def benchmark_detection(video_path: str, duration: int = 60, device: str = "cuda"):
    """
    Benchmark detection module.
    
    Args:
        video_path: Path to video file
        duration: Duration to run benchmark in seconds
        device: Device to use (cuda/cpu)
    """
    print("=" * 60)
    print("Benchmarking Detection Module")
    print("=" * 60)
    
    # Initialize components
    sensor = SensorDataCollector(
        video_source=video_path,
        fps=30,
        enable_stabilization=False,
        imgsz=640
    )
    await sensor.initialize()
    
    detector = ObjectDetector(
        model_path="yolov8n.pt",
        confidence_threshold=0.5,
        device=device,
        half_precision=(device == "cuda")
    )
    detector.initialize()
    
    # Benchmark
    start_time = time.time()
    frame_count = 0
    inference_times = []
    
    while time.time() - start_time < duration:
        frame_data = await sensor.get_frame()
        if frame_data is None:
            break
        
        frame, metadata = frame_data
        
        # Measure inference time
        t0 = time.time()
        detections = detector.detect(frame, metadata)
        t1 = time.time()
        
        inference_times.append((t1 - t0) * 1000)  # ms
        frame_count += 1
    
    elapsed = time.time() - start_time
    
    # Results
    print(f"\nResults:")
    print(f"  Frames processed: {frame_count}")
    print(f"  Duration: {elapsed:.2f}s")
    print(f"  Average FPS: {frame_count / elapsed:.2f}")
    print(f"  Average inference time: {np.mean(inference_times):.2f}ms")
    print(f"  Min inference time: {np.min(inference_times):.2f}ms")
    print(f"  Max inference time: {np.max(inference_times):.2f}ms")
    print(f"  Std inference time: {np.std(inference_times):.2f}ms")
    
    await sensor.close()


async def benchmark_tracking(video_path: str, duration: int = 60, device: str = "cuda"):
    """
    Benchmark tracking module.
    
    Args:
        video_path: Path to video file
        duration: Duration to run benchmark in seconds
        device: Device to use (cuda/cpu)
    """
    print("\n" + "=" * 60)
    print("Benchmarking Tracking Module")
    print("=" * 60)
    
    # Initialize components
    sensor = SensorDataCollector(
        video_source=video_path,
        fps=30,
        enable_stabilization=False,
        imgsz=640
    )
    await sensor.initialize()
    
    detector = ObjectDetector(
        model_path="yolov8n.pt",
        confidence_threshold=0.5,
        device=device,
        half_precision=(device == "cuda")
    )
    detector.initialize()
    
    tracker = ByteTracker(
        track_thresh=0.5,
        track_buffer=90,
        match_thresh=0.8
    )
    
    # Benchmark
    start_time = time.time()
    frame_count = 0
    total_tracks = 0
    max_tracks = 0
    
    while time.time() - start_time < duration:
        frame_data = await sensor.get_frame()
        if frame_data is None:
            break
        
        frame, metadata = frame_data
        
        # Detection + Tracking
        detections = detector.detect(frame, metadata)
        tracks = tracker.update(detections, metadata)
        
        total_tracks += len(tracks)
        max_tracks = max(max_tracks, len(tracks))
        frame_count += 1
    
    elapsed = time.time() - start_time
    
    # Results
    print(f"\nResults:")
    print(f"  Frames processed: {frame_count}")
    print(f"  Duration: {elapsed:.2f}s")
    print(f"  Average FPS: {frame_count / elapsed:.2f}")
    print(f"  Total unique tracks: {tracker.total_tracks}")
    print(f"  Average tracks per frame: {total_tracks / frame_count:.2f}")
    print(f"  Max simultaneous tracks: {max_tracks}")
    print(f"  ID switches: {tracker.id_switches}")
    print(f"  ID switch rate: {tracker.id_switches / frame_count * 100:.3f}%")
    
    await sensor.close()


async def benchmark_end_to_end(video_path: str, duration: int = 60, device: str = "cuda"):
    """
    Benchmark end-to-end pipeline latency.
    
    Args:
        video_path: Path to video file
        duration: Duration to run benchmark in seconds
        device: Device to use (cuda/cpu)
    """
    print("\n" + "=" * 60)
    print("Benchmarking End-to-End Pipeline")
    print("=" * 60)
    
    # Initialize components
    sensor = SensorDataCollector(
        video_source=video_path,
        fps=30,
        enable_stabilization=True,
        imgsz=640
    )
    await sensor.initialize()
    
    detector = ObjectDetector(
        model_path="yolov8n.pt",
        confidence_threshold=0.5,
        device=device,
        half_precision=(device == "cuda")
    )
    detector.initialize()
    
    tracker = ByteTracker()
    
    # Benchmark
    start_time = time.time()
    frame_count = 0
    latencies = []
    
    while time.time() - start_time < duration:
        t0 = time.time()
        
        # Full pipeline
        frame_data = await sensor.get_frame()
        if frame_data is None:
            break
        
        frame, metadata = frame_data
        detections = detector.detect(frame, metadata)
        tracks = tracker.update(detections, metadata)
        
        t1 = time.time()
        latencies.append((t1 - t0) * 1000)  # ms
        frame_count += 1
    
    elapsed = time.time() - start_time
    
    # Results
    print(f"\nResults:")
    print(f"  Frames processed: {frame_count}")
    print(f"  Duration: {elapsed:.2f}s")
    print(f"  Average FPS: {frame_count / elapsed:.2f}")
    print(f"  Average latency: {np.mean(latencies):.2f}ms")
    print(f"  Min latency: {np.min(latencies):.2f}ms")
    print(f"  Max latency: {np.max(latencies):.2f}ms")
    print(f"  P95 latency: {np.percentile(latencies, 95):.2f}ms")
    print(f"  P99 latency: {np.percentile(latencies, 99):.2f}ms")
    
    await sensor.close()


async def main():
    """Main benchmark runner."""
    parser = argparse.ArgumentParser(description='Benchmark Daemon Vision')
    parser.add_argument('--video', type=str, required=True, help='Path to video file')
    parser.add_argument('--duration', type=int, default=60, help='Duration in seconds')
    parser.add_argument('--device', type=str, default='cuda', choices=['cuda', 'cpu'])
    parser.add_argument('--module', type=str, choices=['detection', 'tracking', 'e2e', 'all'], default='all')
    
    args = parser.parse_args()
    
    if not Path(args.video).exists():
        print(f"Error: Video file not found: {args.video}")
        return
    
    print(f"Hardware: {args.device.upper()}")
    print(f"Video: {args.video}")
    print(f"Duration: {args.duration}s\n")
    
    if args.module in ['detection', 'all']:
        await benchmark_detection(args.video, args.duration, args.device)
    
    if args.module in ['tracking', 'all']:
        await benchmark_tracking(args.video, args.duration, args.device)
    
    if args.module in ['e2e', 'all']:
        await benchmark_end_to_end(args.video, args.duration, args.device)
    
    print("\n" + "=" * 60)
    print("Benchmark Complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
