#!/bin/bash

EC2_USER="ec2-user"
EC2_IP="your-ec2-ip"

echo "Stopping existing containers..."
ssh -o StrictHostKeyChecking=no -i key.pem $EC2_USER@$EC2_IP "docker-compose down"

echo "Pulling latest Docker images..."
ssh -o StrictHostKeyChecking=no -i key.pem $EC2_USER@$EC2_IP "docker pull ${{ secrets.DOCKER_USERNAME }}/django-app:latest"

echo "Starting Django container..."
ssh -o StrictHostKeyChecking=no -i key.pem $EC2_USER@$EC2_IP "docker-compose up -d"
