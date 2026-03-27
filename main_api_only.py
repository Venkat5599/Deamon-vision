"""
Daemon Vision - API Server Only Mode
Starts the API server and waits for video upload.
"""
import asyncio
import logging
import uvicorn
from src.modules.api import DaemonVisionAPI

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Run API server only."""
    logger.info("=" * 60)
    logger.info("Daemon Vision - API Server Mode")
    logger.info("PT. Daemon Blockint Technologies")
    logger.info("=" * 60)
    logger.info("Starting API server...")
    logger.info("Waiting for video upload at http://localhost:8000")
    logger.info("Upload a video to start processing")
    logger.info("=" * 60)
    
    # Create API instance
    api = DaemonVisionAPI(
        host="0.0.0.0",
        port=8000,
        cors_origins=["*"]
    )
    
    # Run API server
    config = uvicorn.Config(
        api.app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
    server = uvicorn.Server(config)
    
    try:
        await server.serve()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutdown complete")
