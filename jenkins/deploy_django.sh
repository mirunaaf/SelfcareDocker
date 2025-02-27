#!/bin/bash

EC2_USER="ec2-user"
EC2_IP="18.169.247.44"
SSH_KEY="/var/lib/jenkins/.ssh/id_rsa"

echo "Copying docker-compose.yml to deployment server..."
scp -i $SSH_KEY docker-compose.yml $EC2_USER@$EC2_IP:~/docker-compose.yml

echo "Stopping existing containers on deployment server..."
ssh -o StrictHostKeyChecking=no -i $SSH_KEY $EC2_USER@$EC2_IP "docker-compose down"

echo "Pulling latest Docker images..."
ssh -o StrictHostKeyChecking=no -i $SSH_KEY $EC2_USER@$EC2_IP "docker pull $DOCKER_USERNAME/django-app:latest"

echo "Starting Django container..."
ssh -o StrictHostKeyChecking=no -i $SSH_KEY $EC2_USER@$EC2_IP "docker-compose up -d"
