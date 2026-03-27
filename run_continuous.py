"""
Daemon Vision - Continuous Mode
Keeps API server running and allows multiple video uploads.
"""
import asyncio
import logging
from pathlib import Path
from src.pipeline import DaemonVisionPipeline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Run in continuous mode."""
    logger.info("=" * 60)
    logger.info("Daemon Vision - Continuous Mode")
    logger.info("PT. Daemon Blockint Technologies")
    logger.info("=" * 60)
    
    # Check if uploaded video exists
    video_path = Path("data/uploaded_video.mp4")
    if not video_path.exists():
        logger.warning("No uploaded video found. Please upload a video first.")
        logger.info("Starting API server only...")
        from main_api_only import main as api_main
        await api_main()
        return
    
    logger.info(f"Processing video: {video_path}")
    logger.info("Device: CPU")
    logger.info("=" * 60)
    
    # Initialize pipeline
    pipeline = DaemonVisionPipeline()
    
    try:
        # Override device to CPU
        pipeline.config['detection']['device'] = 'cpu'
        
        await pipeline.initialize()
        
        # Run pipeline - it will process the video
        logger.info("Starting video processing...")
        await pipeline.run()
        
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
    finally:
        logger.info("Video processing complete!")
        logger.info("=" * 60)
        logger.info("To process another video:")
        logger.info("1. Upload a new video through the frontend")
        logger.info("2. Restart this script")
        logger.info("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutdown complete")
