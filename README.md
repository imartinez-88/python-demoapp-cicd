# Python Flask CI/CD Pipeline (Docker + AWS EC2)

## Purpose
This project demonstrates a **fully automated CI/CD pipeline** that takes a Python Flask application from source code to a **live, publicly accessible cloud deployment** using:

- GitLab CI/CD
- Docker images
- AWS EC2 (Ubuntu)
- SSH-based deployment
- Environment variables and secrets

The goal is to understand **end-to-end deployment flow**, not just application code.
Not need for port forwarding, tunneling or curl.

---

## Final Result (Observable Output)

http://18.216.249.197/


```text
# Technology Used: 

  Python 3.9 / 3.10 
  Fask 
  Gunicon 
  Docker
  Gitlab CI/CD
  AWS EC2 (Ubunto) 
  SSH (edd25519)
```text

# Project Structure

```text
.
|--.github/workflows/
|--build/
| ╰Dockerfile
|--deploy/
|---src/
| |--app/
| | |--**int**.py
| | |--views.py -- allows MAC native users to bypass cpuinfo
| | |--templates/
| | |--static/
| |--run.py
| |--requirments.txt
|--tests/
|--.gitignore
|--.gitlab-ci.yml
|--Makefile
|--README.md- like actualy how its displayed vertially and not hortizanlly

```text

 Local Setup: 

Assuming source code is ran on a python FLASK, proceed with: brew install python@3.10

# Start evironment: 
python3.10 -m venv src/venv

# source: 
source src/venv/bin/activate

# install dependecies:
pip install --upgrade pip -- being that this demo python project is running on an older python verion: 3.9slim
pip intall -r src/requirments.txt 

# In this case if using an older python pip: 
pip install "jinja<3.0" is required

# As well for venv 
pip install "werkzeug<2.0" "itsdangerous<2.0"

# MAC users possible OS error outputting: 
Exception: py-cpuinfo currently only works on X86 and some ARM/PPC/S390X CPUs.

# Solution inside code visualiser 
  # Open File: 
    src/app/views.py
         - Code: 
             import cpuinfo
         - Replace with:      -- Try Except allows python to execute cpuinfo and handle crash. 
             try: 
                 import cpuinfo
            except: Exception: 
                cpuinfo = None
         - Guard cpufino: 
             if cpuinfo:
                   info = cpuinfo.get_cpu_info()
             else:
                 info = {"brand_raw": "Uknown CPU"} 
          - Save 
         
# now export path 
export PYTHONPATH=src
python src/run.py

# Output will show:
Running on http://0.0.0.0.

** Once its live locally, create or connect account to gitlab create project name and clone data ** 
# Inside navigate to setting; select add variables: save attribute name and key (ed25519)
  # Step - Create SSH_PRIVATE_VARIABLE 

** Step 1 = CI **  

** SSH Key Creation (Needed for deployment ** 

# Create keypair either ed25519 or rsa, in this instance ed25519
ssh-keygen -t ed25519

# View saved id_ed and id_ed.pub 
ls ~/.ssh

# Unmask in order to create variable inside gitlab {SSH_PRIVATE_VARIABLE} 
cat ~/.ssh/id_ed255199.pub 


** STEP 1 = CD ** 
** Assure that variable is saved- Navigate to Gitlab project (CODE) connect to WEB IDE ** 

# Inside connect to project name - add .gityml
# Create first CI test inside yml file for python:3.9-slim 
# Rerfernce Docker image directory: https://hub.docker.com/_/python

stages: # specify test
-
  -test 

run_test:  -- Design job
-
stage: test
image:python3.9-slim
before_script:  
  - apt-get update && apt-get install -y make git   -- python dependecies pip & update
  - python -m pip install --upgrade pip

script: 
-
  - make take
**                                                                                      **

## EXPECTED OUTPUT - GITLAB PIPELINE DEPLOYMENT TEST SUCCESSFUL ## 


** Step 2 = CI Docker ** 

** Create account with Docker - Create Project - USER AND PASSWORD of account owner inside GitLab varibales 
# Gitlab Variable: 
REGISTRY_USER 
# Key: 
username Docker 

# First nagivate to Docker tokens - Create and give name
# 2nd Gitlab Variable: 
REGISTRY_PASS
# Key: 
Docker generated token

# Save USER docker account and project path [username/projectname] & Refernce Docker library to find docker image & docker dind 


** Step 2 = CD ** 
# Moving on to build stage ONLY if build was success - Back into yml in web IDE
# Update
stages:
-  
  - build

variables: 
-
  IMAGE_NAME: [username/projectname]  -- refernce connection to Docker container connection 
  IMAGE_TAG: mydocker1-1.0

run_build:
-
  stage: build
  image: docker:24.0  -- Create docker image inside docker image - Docker daemon allows execution of command pulls on images and data
  services: 
   - docker:24.0-dind -- Services starts at the jobs time as job (run_build) container, servies attributes link together same netwrok or container during execution.
     
variables:
-
  DOCKER_TLS_CERIR:"/certs" - Allows communication from docker cerfcation and authenticate each other 

before_script:
-
    - echo "$REGISTRY_PASS" | docker login -u "$REGISTRY" --password-stdin
script: 
-
    - docker build -t $IMAGE_NAME:$IMAGE_TAGE -f build/Dockerfile .
    - docker push $IMAGE_NAME:$IMAGE_TAG
  
## EXPECTED OUTPUT - SUCCESSFUL TEST DEPLPYMENT ## 



Recap: At this point the main the app is ready to deploy once build and test and successful. This requires an AWS training account to host the app on a EC2 instance. 

** Create AWS account - goal create key pair from local ed25519 output ** 

# Terminal local % 

ssh-keygen -t ED25519 -f ~/.ssh/ec2_gitlab[/choose unique name]  
# Output 
/User/username/.ssh/gitlab_ec2
/Users/username/.ssh/gitlab_ec2.pub

# Nagivate to launch instance, choose keypair created for secure communication for this instance I chose Ubunto.

Step 3 = CI 
# Create a keypair inside AWS, download key pair .pem file - give it a name in use case {aws1-key.pem}
# Assure its in a .ssh folder Terminal %
mkdir -p ~/.ssh                                   -- Create a folder 
mv ~/Downloads/aws1-key.pem ~/.ssh/aws1-key.pem   -- Move pem file from downloads or whevever it is to .ssh 
chmod 400 ~/.ssh/aws1-key.pem                     -- Secure key 
ls -ls ~/.ssh/aws1-key.pem                        -- Confirm its saved
# test SSH to EC2 Terminal % 
ssh -i ~/.ssh/aws1-key.pem ubunto@EC2_PUBLIC_IP

# Cat .pem Terminal % 
cat ~/.ssh/aws1-key.pem

# Copy output into gitlab variable you make named EC2_SSH_KEY (masked) public
# Add EC2_HOST = public EC2 intance IP 
# Add EC2_USEER = Ubunto 

Step 3 = CD 
** Now that we have desird varibles to boilerplate CI/CD will host out FLASK onto the EC2 instance via SSH ** 
# Navgiate back to Web IDE to run deplpy job

script:
  -
  - deploy


deploy_run: 
  - 
  stage: deploy
  image: alpine:3.19

before_script: 
  - 
  - apk add --no-cache openssh                           -- To skip prompt (fingerprint(yes/no)
  - mkdir -p ~/.ssh                                      -- Path to .ssh
  - printf "%s\n" "$EC2_SSH_KEY" > ~/.ssh/id_ed25519     -- printf allows string to be followed by new line
  - chmod 600 ~/.ssh/id_ed25519
  - ssh-keyscan -H "$EC2_HOST" >> ~/.ssh/known_hosts     -- Trust scan each host line by line  
   
script: 
  - 
    ssh $EC2_USER@EC2_HOST <<EOF
      docker pull $IMAGE_NAME:$IMAGE_TAG
      docker stop myapp || true                          -- Stop Docker image and container 
      docker run myapp || true                           -- Run New image and latest container name 
      docker run -d \
        --name myapp \
        -p 80:5000 \ 
        $IMAGE_NAME:$IMAGE_TAG
    EOF


## EXPECTED OUTPUT DEPLOY SUCCESSUFUL ON EC2 HOST ## 











