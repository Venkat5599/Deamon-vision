# 🚀 Deployment Guide - Daemon Vision Online

## Deployment Options

### Option 1: AWS EC2 with GPU (Recommended)
**Best for**: Production, scalability, GPU acceleration
**Cost**: ~$500-1500/month

### Option 2: Google Cloud Platform (GCP)
**Best for**: AI/ML workloads, good GPU options
**Cost**: ~$400-1200/month

### Option 3: Vast.ai / RunPod
**Best for**: Budget GPU hosting
**Cost**: ~$100-300/month

### Option 4: Railway / Render (CPU Only)
**Best for**: Demo/testing without GPU
**Cost**: ~$20-50/month

---

## 🎯 Option 1: AWS EC2 with GPU (RECOMMENDED)

### Step 1: Choose Instance Type

| Instance | GPU | vCPU | RAM | Cost/hour | Best For |
|----------|-----|------|-----|-----------|----------|
| g4dn.xlarge | T4 (16GB) | 4 | 16GB | $0.526 | Development |
| g4dn.2xlarge | T4 (16GB) | 8 | 32GB | $0.752 | Production |
| g5.xlarge | A10G (24GB) | 4 | 16GB | $1.006 | High Performance |

**Recommended**: g4dn.xlarge ($380/month) for production

### Step 2: Launch Instance

```bash
# 1. Go to AWS Console → EC2 → Launch Instance
# 2. Choose: Deep Learning AMI (Ubuntu 20.04)
# 3. Instance type: g4dn.xlarge
# 4. Storage: 100GB SSD
# 5. Security Group: Open ports 80, 443, 8000, 3001
```

### Step 3: Connect and Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### Step 4: Deploy Application

```bash
# Clone your repository
git clone https://github.com/yourusername/daemon-vision.git
cd daemon-vision

# Build and run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Step 5: Setup Domain and SSL

```bash
# Install Nginx
sudo apt install nginx -y

# Install Certbot for SSL
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Configure Nginx (see nginx config below)
```

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/daemon-vision
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket
    location /stream {
        proxy_pass http://localhost:8000/stream;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }
}
```

---

## 🎯 Option 2: Google Cloud Platform (GCP)

### Step 1: Create VM with GPU

```bash
# Using gcloud CLI
gcloud compute instances create daemon-vision \
    --zone=us-central1-a \
    --machine-type=n1-standard-4 \
    --accelerator=type=nvidia-tesla-t4,count=1 \
    --image-family=pytorch-latest-gpu \
    --image-project=deeplearning-platform-release \
    --boot-disk-size=100GB \
    --maintenance-policy=TERMINATE

# SSH into instance
gcloud compute ssh daemon-vision --zone=us-central1-a
```

### Step 2: Setup (Same as AWS)
Follow AWS steps 3-5 above.

**Cost**: ~$400-600/month with T4 GPU

---

## 🎯 Option 3: Vast.ai / RunPod (Budget Option)

### Vast.ai Setup

```bash
# 1. Go to https://vast.ai
# 2. Search for: RTX 4060 or RTX 3060
# 3. Filter: PyTorch, CUDA 11.8
# 4. Rent instance (~$0.20-0.40/hour)

# SSH into instance
ssh -p PORT root@IP

# Clone and run
git clone https://github.com/yourusername/daemon-vision.git
cd daemon-vision
docker-compose up -d
```

**Cost**: ~$150-300/month

---

## 🎯 Option 4: Railway / Render (CPU Only - Demo)

### Railway Deployment

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Deploy
railway up
```

### Render Deployment

```yaml
# render.yaml
services:
  - type: web
    name: daemon-vision-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py --device cpu
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0

  - type: web
    name: daemon-vision-frontend
    env: node
    buildCommand: cd frontend && npm install && npm run build
    startCommand: cd frontend && npm run preview
```

**Cost**: ~$20-50/month (CPU only, slower)

---

## 📦 Docker Compose for Production

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DEVICE=cuda
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3001:3001"
    environment:
      - VITE_API_URL=https://yourdomain.com/api
      - VITE_WS_URL=wss://yourdomain.com/stream
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - /etc/letsencrypt:/etc/letsencrypt
    depends_on:
      - backend
      - frontend
    restart: unless-stopped
```

---

## 🔒 Security Checklist

- [ ] Enable HTTPS/SSL
- [ ] Setup firewall rules
- [ ] Use environment variables for secrets
- [ ] Enable CORS properly
- [ ] Add rate limiting
- [ ] Setup monitoring (CloudWatch/Datadog)
- [ ] Regular backups
- [ ] Update dependencies regularly

---

## 📊 Cost Comparison

| Platform | GPU | Monthly Cost | Setup Time | Best For |
|----------|-----|--------------|------------|----------|
| AWS EC2 | T4 | $380-750 | 2-3 hours | Production |
| GCP | T4 | $400-600 | 2-3 hours | AI/ML |
| Vast.ai | RTX 4060 | $150-300 | 1 hour | Budget |
| Railway | None | $20-50 | 30 min | Demo |

---

## 🚀 Quick Deploy Script

```bash
#!/bin/bash
# deploy.sh

echo "🚀 Deploying Daemon Vision..."

# Pull latest code
git pull origin main

# Build Docker images
docker-compose -f docker-compose.prod.yml build

# Stop old containers
docker-compose -f docker-compose.prod.yml down

# Start new containers
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

echo "✅ Deployment complete!"
echo "Frontend: https://yourdomain.com"
echo "Backend: https://yourdomain.com/api"
echo "Docs: https://yourdomain.com/api/docs"
```

---

## 📝 Environment Variables

```bash
# .env.production
DEVICE=cuda
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://yourdomain.com
MAX_UPLOAD_SIZE=100MB
REDIS_URL=redis://redis:6379
```

---

## 🎯 Recommended: AWS EC2 Setup

**Total Time**: 2-3 hours
**Monthly Cost**: ~$380 (g4dn.xlarge)
**Performance**: Excellent (T4 GPU)

### Quick Start Commands

```bash
# 1. Launch EC2 instance (g4dn.xlarge)
# 2. SSH in
ssh -i key.pem ubuntu@your-ip

# 3. Run setup script
curl -fsSL https://raw.githubusercontent.com/yourusername/daemon-vision/main/setup-aws.sh | bash

# 4. Deploy
cd daemon-vision
docker-compose -f docker-compose.prod.yml up -d

# 5. Setup domain
sudo certbot --nginx -d yourdomain.com
```

---

## ✅ Post-Deployment Checklist

- [ ] Test frontend: https://yourdomain.com
- [ ] Test API: https://yourdomain.com/api/health
- [ ] Test WebSocket: Check video streaming
- [ ] Upload test video
- [ ] Monitor GPU usage
- [ ] Check logs for errors
- [ ] Setup monitoring/alerts
- [ ] Configure backups

---

**Ready to deploy? I recommend AWS EC2 with g4dn.xlarge for the best balance of performance and cost!** 🚀
