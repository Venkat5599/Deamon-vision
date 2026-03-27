#!/bin/bash
# Daemon Vision Setup Script

echo "=========================================="
echo "Daemon Vision Setup"
echo "=========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Download YOLOv8 model
echo "Downloading YOLOv8 model..."
python3 -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# Create necessary directories
echo "Creating directories..."
mkdir -p data logs

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To run Daemon Vision:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Place your video in data/ folder"
echo "  3. Run: python main.py --video data/your_video.mp4"
echo ""
echo "To run with Docker:"
echo "  docker-compose up --build"
echo ""
