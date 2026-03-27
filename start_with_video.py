"""
Daemon Vision - Start with Video Processing
Starts the full pipeline with API server and video processing.
"""
import asyncio
import logging
import sys
import uvicorn
from pathlib import Path

from src.pipeline import DaemonVisionPipeline
from src.modules.api import DaemonVisionAPI

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('daemon_vision.log')
    ]
)
logger = logging.getLogger(__name__)


async def main():
    """Run full system with video processing."""
    logger.info("=" * 60)
    logger.info("Daemon Vision - Full System with Video Processing")
    logger.info("PT. Daemon Blockint Technologies")
    logger.info("=" * 60)
    
    try:
        # Initialize pipeline
        pipeline = DaemonVisionPipeline(config_path='config.yaml')
        
        # Override video source to use uploaded video
        video_path = "data/uploaded_video.mp4"
        if Path(video_path).exists():
            pipeline.config['sensor']['video_source'] = video_path
            logger.info(f"Using video: {video_path}")
        else:
            logger.warning(f"Video not found: {video_path}")
            logger.info("System will wait for video upload")
        
        # Force CUDA
        pipeline.config['detection']['device'] = 'cuda'
        logger.info("Device: CUDA")
        
        # Initialize pipeline
        await pipeline.initialize()
        
        # Pipeline already has API initialized and connected
        logger.info("=" * 60)
        logger.info("System ready!")
        logger.info("Frontend: http://localhost:3001")
        logger.info("Backend API: http://localhost:8000")
        logger.info("API Docs: http://localhost:8000/docs")
        logger.info("=" * 60)
        
        # Run pipeline (includes API server)
        await pipeline.run()
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
