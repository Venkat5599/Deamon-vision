#!/bin/bash

echo "🚀 Deploying Daemon Vision..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Pull latest code (if using git)
if [ -d ".git" ]; then
    echo "📥 Pulling latest code..."
    git pull origin main
fi

# Build Docker images
echo "🔨 Building Docker images..."
docker-compose -f docker-compose.prod.yml build

# Stop old containers
echo "🛑 Stopping old containers..."
docker-compose -f docker-compose.prod.yml down

# Start new containers
echo "▶️  Starting new containers..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check status
echo "📊 Checking container status..."
docker-compose -f docker-compose.prod.yml ps

# Check health
echo "🏥 Checking health..."
curl -f http://localhost:8000/health || echo "⚠️  Backend health check failed"
curl -f http://localhost:3001 || echo "⚠️  Frontend health check failed"

echo ""
echo "✅ Deployment complete!"
echo "Frontend: http://localhost:3001"
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "To view logs: docker-compose -f docker-compose.prod.yml logs -f"
