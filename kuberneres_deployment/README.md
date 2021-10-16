# How to deploy using Kubernetes

## Steps to replicate

1. Make sure you have kubectl ad k3d installed on your computer. 
2. Create a new cluster for your deployment
    ```
    k3d cluster create todo-cluster -p "8081:8080@loadbalancer"
    # this command is creating a new cluster which is mapping the localhost 8081 port to port 8080 of the cluster load balancer
    # this is what allows us to access the load balancer
    ```
3. Create a yaml file for your deployment.
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-deployment
spec:
  selector:
    matchLabels:
      app: flask-todo-app
  replicas: 1
  template:
    metadata:
      labels:
        app: flask-todo-app
    spec:
      containers:  
      - name: todo-container
        image: zcyrus/todo-flask:latest # pulls image from my dockerhub
        ports:
          - containerPort: 5000 # our flask app is open on port 5000 and so is our container.
```

4. Use kubectl to create a new resource/pod from our new deployment file 
```
kubectl create -f {name of yaml file}.yaml
```

5. Use kubectl expose to expose a new resource as a new Kubernetes service.
```
kubectl expose deployment {name of deployment} --port 8080 --target-port 5000 --type=LoadBalancer
```

6. Navigate to localhost:8081 to view your todo application served by Kubernetes. 