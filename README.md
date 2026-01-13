# Python Flask CI/CD Pipeline (Docker + AWS EC2)

# Purpose
This project demonstrates a fully automated **CI/CD pipeline that takes a Python Flask application from source code to a live, publicly accessible cloud deployment using**:

- GitLab CI/CD
- Docker images
- AWS EC2 (Ubuntu)
- SSH-based deployment
- Environment variables and secrets

The goal is to understand **end-to-end deployment flow**, not just application code.
Not need for port forwarding, tunneling or curl.

# Final Result (Live Deployment)
http://18.216.249.197/



## Technology Used: 
  Python 3.9 / 3.10 
  Fask 
  Gunicon 
  Docker
  GitLab CI/CD
  AWS EC2 (Ubunto) 
  SSH (edd25519)



## Project Structure

<pre>
.
├── .github/
│   └── workflows/
│
├── build/
│   └── Dockerfile
│
├── deploy/
│
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── views.py      -- Allows macOS users to bypass cpuinfo 
│   │   ├── templates/
│   │   └── static/
│   │
│   ├── run.py
│   └── requirements.txt  -- Establishes rules 
│
├── tests/
├── .gitignore
├── .gitlab-ci.yml
├── Makefile             -- Host many languages being used at once
└── README.md
</pre>


## Local Setup: Terminal

brew install python@3.10


## Create virtual evironment: 
python3.10 -m venv src/venv
source src/venv/bin/activate

## Install dependecies:
pip install --upgrade pip 
pip intall -r src/requirments.txt 

## Older python base image: 
pip install "jinja<3.0" "werkzeug<2.0" "itsdangerous<2.0"


## macOS cpuinfo compatibility Fix: maxOS may raise 
Exception: py-cpuinfo currently only works on X86 and some ARM/PPC/S390X CPUs.

# Solution 
<pre>
   Open File: 
    src/app/views.py
         - Replace: 
             import cpuinfo
  
         - With:   
             try: 
                 import cpuinfo
            except: Exception: 
                cpuinfo = None
  
         - Guard usage: 
             if cpuinfo:
                   info = cpuinfo.get_cpu_info()
             else:
                 info = {"brand_raw": "Uknown CPU"} 
  
* Run Locally *
export PYTHONPATH=src
python src/run.py
 </pre>


## Output will show:
Running on http://0.0.0.0.



# CI/CD Overview 
<pre> 
  The pipeline is split into three stages: 
  
    - Test CI - Validating applications
    - Build CI - Build and push Docker Images
    - Deploy CD - SSH deploy to AWS EC2 
  </pre>


# Step 1 - Test Stage
Base Image: 
   - python:3.9-slim
# Test push: .gitlab-ci.yml
<pre> 
    stages:
         test
    run_test:
         stage: test
         image: python:3.9-slim
     before_script:
         - apt-get update && apt-get install -y make git
         - python -m pip install --upgrade pip
     script:
         - make test
</pre>

## Expected Result: Gitlab pipeline test stage succeeded! 


# Step 2 - CI/CD Docker Build & Push
## Create Variables: 
  REGISTRY_USER > Docker username 
  REGISTRY_PASS > Docker access token

## Build Config: .gitlab-ci.yml
<pre> 
stages: 
  - build

run_build: 
  stage: build
  image: docker:24.0
  services: 
    - docker:24.0-dind
  varibales: 
    DOCKER_TLS_CERDIR: "/certs"
  
before_script:
    - echo "$REGISTRY_PASS | docker login -u "$REGISTRY_USER" --password-stdin
script:
  - docker build -t $IMAGE_NAME:$IMAGE_TAG -f build/Dockerfile . 
  - docker push $IMAGE_NAME:$IMAGE_TAG
</pre>

## Expected Result: Docker Image Successfully pushed to registry 

# Step 3 - AWS EC2 Setup 
## Create SSH key 
ssh-keygen -t ED25519 -f ~/.ssh/ec2_gitlab  
## Output 
/User/username/.ssh/gitlab_ec2
/Users/username/.ssh/gitlab_ec2.pub

## Launch EC2 Istance 
<pre> 
OS: Ubuntu 
Attach keypair 
Open Port 80 /5000 (your chose ports)
</pre>

## Store Secerets inside Gitlab Setting > Variabels
<pre> 
EC2_SSH_KEY = Private key content linking AWS instance ~/.ssh 
EC2_HOST = EC2 public IP 
EC2_USER = ubuntu
</pre>


# Step 4 - CD Deployment to EC2
## Deploy Job: .gitlab-ci.yml
<pre> 
stages:
  - deploy

deploy_run: 
  stage: deplpoy
  image: alpine:3.19 
  before_script: 
    - apk add --no-cache openssh 
    - mkdir -p ~/.ssh
    - printf "%s\n" "$EC2_SSH_KEY" > ~/.ssh/id_ed25519
    - chmod 600 ~/.ssh/id_ed25519
    - ssh-keyscan -H "$EC2_HOST" >> ~/.ssh/known_hosts
script: 
    - shh $EC2_USER@EC2_HOST
</pre>
## Expected Result: Applicaiton Live on EC2 

# What This Project Demonstrates

END-to-END CI/CD ownership 
Dockerized Python services 
Secure SSH-based cloud deployment
Secrets managment via Gitlab variables
Cloud infrastructure oversight 

