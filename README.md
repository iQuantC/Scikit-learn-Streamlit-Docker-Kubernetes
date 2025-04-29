# Prototype Scikit-learn ML Model with Streamlit App

## Requirements
1. Python
2. Streamlit
3. Docker
4. DockerHub Account
5. Kubernetes Cluster (Minikube)


## Install Required Packages
```sh
sudo apt update && sudo apt upgrade -y
```
```sh
sudo apt install python3-pip -y
```

## Create Python Virtual Environment & Activate it
```sh
python -m venv venv
source venv/bin/activate
```

```sh
pip3 install streamlit scikit-learn pandas matplotlib seaborn reportlab
```

## Run Streamlit App
```sh
streamlit run app.py
```

## On your browser
```sh
http://localhost:8501
```
or 
```sh
http://PublicIP:8501
```

## Build and Run the Docker Image Using the Dockerfile
```sh
docker build -t streamlit-ml-app:latest .
```
```sh
docker run -p 8501:8501 streamlit-ml-app:latest
```

## On your browser
```sh
http://localhost:8501
```



## Push Streamlit Docker Image to DockerHub

Go to your DockerHub account and create a Personal Access Token (PAT) - This will be your password - 
```sh
docker login -u iquantc
```

### Tag Your Local Docker Image
```sh
docker tag streamlit-ml-app:latest iquantc/streamlit-ml-app:latest
```

### Push the Image to DockerHub
```sh
docker push iquantc/streamlit-ml-app:latest
```


## Deploy Streamlit App Docker Image from DockerHub to Kubernetes

Review manifest files

### Create Minikube cluster
```sh
minikube start --driver=docker
```

### Deploy the Kubernetes Manifest Files

```sh
kubectl apply -f deployment.yaml
```
```sh
kubectl apply -f service.yaml
```

### Check the Resources Created
```sh
kubectl get pods
```
```sh
kubectl get svc
```
```sh
minikube ip
```

### Open in Browser

```sh
http://<minikube-ip>:30001
```



## Clean up

```sh
minikube stop
```
```sh
minikube delete --all
```
