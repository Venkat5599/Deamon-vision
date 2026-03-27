# 🚀 Deploy Daemon Vision Online - Quick Start

## Fastest Way to Deploy (AWS EC2)

### Step 1: Launch EC2 Instance (5 minutes)

1. Go to [AWS Console](https://console.aws.amazon.com/ec2/)
2. Click "Launch Instance"
3. Configure:
   - **Name**: daemon-vision
   - **AMI**: Deep Learning AMI (Ubuntu 20.04)
   - **Instance type**: g4dn.xlarge (T4 GPU)
   - **Key pair**: Create new or use existing
   - **Storage**: 100GB gp3
   - **Security Group**: 
     - SSH (22) - Your IP
     - HTTP (80) - Anywhere
     - HTTPS (443) - Anywhere
     - Custom TCP (8000) - Anywhere
     - Custom TCP (3001) - Anywhere

4. Click "Launch Instance"

**Cost**: ~$0.526/hour (~$380/month)

### Step 2: Connect to Instance (2 minutes)

```bash
# Download your key pair (if new)
chmod 400 your-key.pem

# Connect via SSH
ssh -i your-key.pem ubuntu@YOUR-INSTANCE-IP
```

### Step 3: Run Setup Script (10 minutes)

```bash
# Download and run setup script
curl -fsSL https://raw.githubusercontent.com/yourusername/daemon-vision/main/setup-aws.sh -o setup.sh
chmod +x setup.sh
./setup.sh

# Logout and login again (for Docker group)
exit
ssh -i your-key.pem ubuntu@YOUR-INSTANCE-IP
```

### Step 4: Deploy Application (5 minutes)

```bash
# Clone your repository
git clone https://github.com/yourusername/daemon-vision.git
cd daemon-vision

# Make deploy script executable
chmod +x deploy.sh

# Deploy!
./deploy.sh
```

### Step 5: Setup Domain (Optional, 5 minutes)

```bash
# Point your domain to the instance IP
# Then run:
sudo certbot --nginx -d yourdomain.com

# Copy nginx config
sudo cp nginx-production.conf /etc/nginx/sites-available/daemon-vision
sudo ln -s /etc/nginx/sites-available/daemon-vision /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 6: Access Your Application! 🎉

- **Frontend**: http://YOUR-INSTANCE-IP:3001
- **Backend API**: http://YOUR-INSTANCE-IP:8000
- **API Docs**: http://YOUR-INSTANCE-IP:8000/docs

Or with domain:
- **Frontend**: https://yourdomain.com
- **Backend API**: https://yourdomain.com/api
- **API Docs**: https://yourdomain.com/api/docs

---

## Alternative: Budget Option (Vast.ai)

### Step 1: Create Account
1. Go to [Vast.ai](https://vast.ai)
2. Sign up and add credits ($10-20)

### Step 2: Rent GPU Instance
1. Search for: "RTX 4060" or "RTX 3060"
2. Filter: PyTorch, CUDA 11.8, Ubuntu
3. Sort by: Price (lowest first)
4. Click "Rent" (~$0.20-0.40/hour)

### Step 3: Connect and Deploy
```bash
# SSH into instance (use provided command)
ssh -p PORT root@IP

# Clone and deploy
git clone https://github.com/yourusername/daemon-vision.git
cd daemon-vision
chmod +x deploy.sh
./deploy.sh
```

**Cost**: ~$150-300/month

---

## Monitoring Your Deployment

### Check Container Status
```bash
docker-compose -f docker-compose.prod.yml ps
```

### View Logs
```bash
# All logs
docker-compose -f docker-compose.prod.yml logs -f

# Backend only
docker-compose -f docker-compose.prod.yml logs -f backend

# Frontend only
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### Check GPU Usage
```bash
nvidia-smi
```

### Restart Services
```bash
docker-compose -f docker-compose.prod.yml restart
```

---

## Troubleshooting

### Backend not starting?
```bash
# Check logs
docker logs daemon-vision-backend

# Check GPU
nvidia-smi

# Restart
docker-compose -f docker-compose.prod.yml restart backend
```

### Frontend not loading?
```bash
# Check logs
docker logs daemon-vision-frontend

# Rebuild
docker-compose -f docker-compose.prod.yml build frontend
docker-compose -f docker-compose.prod.yml up -d frontend
```

### WebSocket not connecting?
- Check firewall rules (port 8000 open)
- Check CORS settings in config.yaml
- Check nginx configuration

---

## Cost Breakdown

### AWS EC2 (g4dn.xlarge)
- Instance: $380/month
- Storage (100GB): $10/month
- Data transfer: $10-50/month
- **Total**: ~$400-440/month

### Vast.ai (RTX 4060)
- GPU rental: $0.20/hour × 730 hours = $146/month
- Storage: Included
- **Total**: ~$150-200/month

### Railway (CPU only - Demo)
- Starter plan: $20/month
- **Total**: ~$20/month (no GPU)

---

## Production Checklist

- [ ] Instance launched and running
- [ ] Docker and NVIDIA toolkit installed
- [ ] Application deployed
- [ ] Health checks passing
- [ ] Domain configured (optional)
- [ ] SSL certificate installed (optional)
- [ ] Firewall rules configured
- [ ] Monitoring setup
- [ ] Backups configured
- [ ] Documentation updated

---

## Quick Commands Reference

```bash
# Deploy
./deploy.sh

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart
docker-compose -f docker-compose.prod.yml restart

# Stop
docker-compose -f docker-compose.prod.yml down

# Update and redeploy
git pull && ./deploy.sh

# Check GPU
nvidia-smi

# Check disk space
df -h

# Check memory
free -h
```

---

## 🎉 You're Live!

Your Daemon Vision system is now deployed online and accessible from anywhere!

**Share with your friend:**
- Frontend URL: http://YOUR-IP:3001
- Show them the live detection and tracking
- Demonstrate the GPU acceleration
- Discuss Lidar integration next steps

**Next Steps:**
1. Test with different videos
2. Monitor performance
3. Setup monitoring/alerts
4. Plan Lidar integration
5. Scale as needed

---

**Total Time**: 30-45 minutes
**Monthly Cost**: $150-440 (depending on platform)
**Status**: 🟢 LIVE AND RUNNING!
