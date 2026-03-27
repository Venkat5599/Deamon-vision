"""
Daemon Vision - Main Entry Point
Real-Time Multi-Target Detection, Tracking & Predictive Locking System
"""
import asyncio
import argparse
import logging
import sys
from pathlib import Path

from src.pipeline import DaemonVisionPipeline


def setup_logging(level: str = "INFO"):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('daemon_vision.log')
        ]
    )


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Daemon Vision - Real-Time Multi-Target Detection & Tracking'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    parser.add_argument(
        '--video',
        type=str,
        help='Override video source from config'
    )
    
    parser.add_argument(
        '--telemetry',
        type=str,
        help='Override telemetry source from config'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--device',
        type=str,
        choices=['cuda', 'cpu'],
        help='Override device for inference'
    )
    
    return parser.parse_args()


async def main():
    """Main entry point."""
    args = parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("Daemon Vision - Multi-Target Detection & Tracking System")
    logger.info("PT. Daemon Blockint Technologies")
    logger.info("=" * 60)
    
    try:
        # Initialize pipeline
        pipeline = DaemonVisionPipeline(config_path=args.config)
        
        # Override config if command line args provided
        if args.video:
            pipeline.config['sensor']['video_source'] = args.video
            logger.info(f"Video source overridden: {args.video}")
        
        if args.telemetry:
            pipeline.config['sensor']['telemetry_source'] = args.telemetry
            logger.info(f"Telemetry source overridden: {args.telemetry}")
        
        if args.device:
            pipeline.config['detection']['device'] = args.device
            logger.info(f"Device overridden: {args.device}")
        
        # Initialize and run
        await pipeline.initialize()
        await pipeline.run()
    
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
