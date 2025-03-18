# DevOps CI/CD Pipeline for Django Application


This project implements a CI/CD pipeline for deploying a Django application using GitHub Actions, Jenkins, Docker, and Ansible on AWS EC2.
## Objectives

- Automate the deployment process using CI/CD tools.
- Containerize the Django application using Docker.
- Use GitHub Actions for building and pushing the Docker image to Docker Hub.
- Deploy the application using Jenkins and Ansible.
- Use AWS EC2 instances for Jenkins and Deployment.


## Technologies Used

- GitHub Actions - Automates the build and push process.
- Docker & Docker Hub - Containerization of the Django application.
- Jenkins - CI/CD orchestration.
- Ansible - Automates server configuration and deployment.
- AWS EC2 - Cloud instances for Jenkins and Deployment.


## Infrastructure Setup

Two AWS EC2 instances were configured, each with a specific role:

🔹 Jenkins Instance (jenkins2)

- Installed Jenkins to orchestrate the deployment.
- Set up SSH keys to securely connect to Deploy Instance.
- Installed Ansible to automate configuration and deployment.
- Installed Git, required for fetching the latest code from the repository.

🔹 Deploy Instance (deploy_django2)

- Runs the containerized Django application.
- Managed by Ansible, which installs Docker, dependencies and starts the containers.

## Connecting the Instances via SSH

1️⃣ Generating the SSH Key on Jenkins


On the Jenkins instance, we generated an SSH key pair (private + public key):
```
ssh-keygen -t rsa -b 4096 -f /var/lib/jenkins/.ssh/id_rsa
```
2️⃣ Copying the Public Key to the Deploy Instance

To allow passwordless authentication, we copied the public key to the Deploy Instance:
```
sudo ssh-copy-id -i /var/lib/jenkins/.ssh/id_rsa.pub ec2-user@DEPLOY_IP
```
This added the public key to the authentication file for the ec2-user on Deploy Instance.

3️⃣ Authenticating from Jenkins to Deploy

When Jenkins connects to the Deploy instance, it uses the private key (id_rsa), which remains local on Jenkins:

```
ssh -i /var/lib/jenkins/.ssh/id_rsa ec2-user@DEPLOY_IP
```

The Deploy server checks if the private key matches the public key in ~/.ssh/authorized_keys and grants access.


## Docker and Docker Compose in Deployment

The Django application is containerized using Docker and managed with Docker Compose. The application runs in a container, ensuring consistency across different environments.

### How They Work in Deployment

1️⃣ Dockerfile is used to define the application environment, installing Python, dependencies, and setting up the Django application.

2️⃣ Docker Compose defines two services required for the application to run, including MySQL as the database and the Django web application container.

3️⃣ The deployment process:

GitHub Actions builds the Docker image and pushes it to Docker Hub.

Jenkins triggers Ansible to configure the Deploy instance.

Ansible pulls the latest Docker image and runs the Django application with MySQL inside containers using Docker Compose.

## CI/CD Workflow with GitHub Actions (ci.yml)

The GitHub Actions pipeline automates the build and push process of the Django application container. The workflow consists of the following jobs:

1️⃣ Build & Push Docker Image:

- Triggers on a push to main branch.

- Logs into Docker Hub using stored credentials.

- Builds the Django application image and tags it as latest.

- Pushes the new image to Docker Hub.

2️⃣ Trigger Jenkins Deployment:

- Ensures the Docker image is available before deployment.

- Triggers Jenkins via API to deploy the latest image using Ansible on AWS EC2.



```
name: CI Pipeline for Django on Amazon Linux

on:
  push:
    branches:
      - main

jobs:
  build_push:
    name: "Build & Push Docker Image"
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Login to Docker Hub
        run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

      - name: Build & Push Docker Image
        run: |
          docker build -t ${{ secrets.DOCKER_USERNAME }}/django-app:latest .
          docker push ${{ secrets.DOCKER_USERNAME }}/django-app:latest

  trigger_jenkins:
    name: "Trigger Jenkins Deployment"
    needs: build_push
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Jenkins Deployment
        run: |
          curl -u "${{ secrets.JENKINS_USERNAME }}:${{ secrets.JENKINS_API_TOKEN }}" -X POST \
          "http://${{ secrets.JENKINS_URL }}/job/deploy-django/build"
```
## Jenkins Deployment Pipeline

-  Jenkins triggers the deployment after the latest Docker image is built and pushed to Docker Hub by GitHub Actions.
- Retrieves the Deploy instance IP from Jenkins credentials.
-  Executes the Ansible playbook, passing the EC2 instance IP dynamically.

```
pipeline {
    agent any
    environment {
        DEPLOY_IP = credentials('DEPLOY_IP')
    }
    stages {
        stage('Deploy with Ansible') {
            steps {
                    sh 'ansible-playbook -i ansible/inventory.ini ansible/playbook.yml --extra-vars "ansible_host=$DEPLOY_IP"'
            }
        }
    }
}
```

## Deploying with Ansible

The Ansible playbook automates the setup and deployment of the Django application on the Deploy instance.

- It ensures that Ansible targets the correct EC2 instance for deployment.
- Updates the system and installs Docker & Docker Compose.
- Configures Docker to run without requiring sudo.
- Fetches the latest docker-compose.yml from GitHub.
- Stops and removes old containers, then pulls the latest Django image from Docker Hub.
- Starts the updated containers, ensuring a fresh deployment.

```
- name: Configure EC2 and Deploy Django App
  hosts: ec2
  become: yes
  vars:
    ansible_host: "{{ ansible_host }}"

  tasks:
    - name: Update package lists
      yum:
        name: '*'
        state: latest

    - name: Install Docker
      yum:
        name: docker
        state: present

    - name: Start Docker service
      service:
        name: docker
        state: started
        enabled: yes

    - name: Add ec2-user to Docker group
      command: usermod -aG docker ec2-user

    - name: Install Docker Compose
      get_url:
        url: "https://github.com/docker/compose/releases/latest/download/docker-compose-Linux-x86_64"
        dest: "/usr/local/bin/docker-compose"
        mode: 'u+x'

    - name: Download latest docker-compose.yml
      get_url:
        url: "https://raw.githubusercontent.com/mirunaaf/SelfcareDocker/main/docker-compose.yml"
        dest: /home/ec2-user/docker-compose.yml
        mode: '0644'

    - name: Deploy containers
      shell: |
        docker-compose down
        docker images --filter "reference=mirunaf/django-app" --format '{{ "{{.ID}}" }}' | xargs -r docker rmi -f
        docker-compose pull
        docker-compose up -d
      args:
        chdir: /home/ec2-user/



