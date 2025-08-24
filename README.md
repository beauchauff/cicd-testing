CI-CD-and_Testing (Assignment 6)

Deploying an entire sentiment analysis system

1. Project Architecture
This sentiment analysis system uses Continuous Integration/Continuous Deployment pipeline uses GitHub Actions to 
automate testing and linting, ensuring code quality prior to deployment. The FastAPI backend serves sentiment
predictions and logs every request and response to the shared docker volume. 
A streamlit monitoring dashboard is a second container which runs a streamlit application to read the logs from the
same shared volume to visualize model performance. A docker volume is used to share log data between the e
FastAPI Prediction Service and the monitoring dashboard. The program 
is launched all on a live cloud server (AWS EC2) with the services as separate docker containers.
-.github
--workflows
---ci.yml
---manual.yml
-api
--Dockerfile
--IMDB Dataset.csv
--main.py
--Makefile
--requirements.txt
--sentiment_model.pkl
--target_names.pkl
--test_api.py
-logs
--prediction_logs.json
-monitoring
--app.py
--Dockerfile
--IMDB Dataset_1.csv
--Makefile
--requirements.txt
--test_dashboard.py
-.gitignore
-README.md

3. Local Development
Build and run containers; create a shared docker volume:
   #Create a shared docker volume
   docker volume create sentimentlogs

   #Build images
   docker build -t sentimentapi . (if in api folder)
   docker build -t sentimentmonitoring ./monitoring

   #Run containers
   docker run -d -p 8000:8000 --name sentimentapi --mount source=sentimentlogs,target=/logs sentimentapi
   docker run -d -p 8501:8501 --name sentimentmonitor --mount source=sentimentlogs,target=/logs sentimentmonitoring
   
4. Manual Deployment Guide
How to launch and configure the EC2 instance and its security group.
A. Launch a t2.micro EC2 instance with Ubuntu
   - Select Compute 
   - Select EC2 
   - Launch an Instance 
   - Name: sentimentMonitoring
   - Choose Ubuntu from quick start
   - Select instance type t2.micro
   - Pick key-pair: vockey
        -download key:pair  
        -name
        -select .pem
        -click Create key pair and note download location  
   - allow SSH traffic from anywhere,
   - leave others as default
   - "launch instance"
B. Configure security group to allow traffic on:
   - From the Navigation Pane, choose Security Groups
   - Create security group with name and description
   - Add 3 inbound rules:
     - TYPE SSH: Port 22(SSH) from your IP address for access
     - TYPE CUSTOM TCP: Port 8000 (this will be used for FastAPI, optional description) from anywhere.
     - TYPE CUSTOM TCP: Port 8501 (to be used for Streamlit) from anywhere.
   - Create security group
C. Connect to security group:
   - Navigating to EC2 instances running
   - select EC2 instance
   - from Actions tab, underneath security, select change security groups 
   - select sentimentgroup from dropdown
   - add and save
D. Connect to EC2 instance using SSH by:
   - Select the running EC2 instance, to copy the public IP address
   - From terminal, ssh -i /path/to/key.pem ubuntu@ <ipaddress> 
E. Set up the Server Environment
    - Install Docker on EC2 instance
        sudo apt update
        sudo apt install docker.io -y
        sudo systemctl start docker
        sudo systemctl enable docker
    -   Install  and clone GitHub  on EC2 instance
        git clone https://github.com/<username>/<repo>.git        
F. Deploy the Application
    -   Create a shared Docker volume on the logs
        sudo docker volume create sentimentlogs
    -   Build images
        docker build -t sentimentapi . (if in api folder)
        docker build -t sentimentmonitoring ./monitoring
    -   Run images in the detached mode
      docker run -d -p 8000:8000 --name sentimentapi --mount source=sentimentlogs,target=/logs sentimentapi
      docker run -d -p 8501:8501 --name sentimentmonitor --mount source=sentimentlogs,target=/logs sentimentmonitor
   



