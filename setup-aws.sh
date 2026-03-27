#!/bin/bash

echo "🚀 Setting up Daemon Vision on AWS EC2..."

# Update system
echo "📦 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install NVIDIA Container Toolkit
echo "🎮 Installing NVIDIA Container Toolkit..."
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Install Docker Compose
echo "📦 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx
echo "🌐 Installing Nginx..."
sudo apt install -y nginx

# Install Certbot
echo "🔒 Installing Certbot..."
sudo apt install -y certbot python3-certbot-nginx

# Install Git
echo "📚 Installing Git..."
sudo apt install -y git

# Clone repository (you'll need to update this URL)
echo "📥 Cloning repository..."
# git clone https://github.com/yourusername/daemon-vision.git
# cd daemon-vision

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Clone your repository: git clone <your-repo-url>"
echo "2. cd daemon-vision"
echo "3. docker-compose -f docker-compose.prod.yml up -d"
echo "4. Setup SSL: sudo certbot --nginx -d yourdomain.com"
