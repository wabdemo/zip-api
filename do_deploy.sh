#!/bin/bash

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io docker-compose

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Clone your project repository (replace with your repo)
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# Build and start the application
sudo docker-compose up -d --build

echo "Application deployed successfully! Access via http://your-droplet-ip/docs"
