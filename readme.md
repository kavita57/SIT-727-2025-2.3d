# **Flask Personal Journal App with MongoDB Atlas**

This is a **Flask-based personal journal application** that allows users to add journal entries, view them, and automatically analyze the sentiment of the content. The application is **containerized using Docker** and can be deployed to **Kubernetes**. It uses **MongoDB Atlas** as a managed database.

---

## **Table of Contents**

1. [Project Overview](#project-overview)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [MongoDB Atlas Setup](#mongodb-atlas-setup)
5. [Flask Application Structure](#flask-application-structure)
6. [Dockerizing the Application](#dockerizing-the-application)
7. [Kubernetes Setup](#kubernetes-setup)
8. [Running the Application](#running-the-application)
9. [Environment Variables](#environment-variables)
10. [Future Improvements](#future-improvements)

---

## **Project Overview**

This project is a **Flask-based web application** that allows users to:

- Write new journal entries with a title and content.
- Analyze the sentiment of the journal entry (positive, neutral, or negative) using **TextBlob**.
- View a list of all journal entries.
- View detailed information about individual journal entries.

The application is designed to be **containerized with Docker** and can be deployed to **Kubernetes**. **MongoDB Atlas** is used as the database service.

---

## **Requirements**

To run this application, the following software is required:

- **Python 3.13.2** (used for development and production)
- **Flask 2.3.2**
- **Flask-PyMongo 2.3.0** (for MongoDB integration)
- **TextBlob 0.17.1** (for sentiment analysis)
- **Docker** (for containerization)
- **Kubernetes** (for orchestration)

---

## **Installation**

### **1. Clone the Repository**

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/flask-journal-app.git
cd flask-journal-app
```

### **2. Install Dependencies**

Create and activate a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

Install the required dependencies using **pip**:

```bash
pip install -r requirements.txt
```

---

## **MongoDB Atlas Setup**

### **1. Create a MongoDB Atlas Account**

1. Visit [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and sign up or log in.
2. Create a **new project** and a **new cluster**.
3. Follow the instructions to connect your application to MongoDB Atlas:
   - **Whitelist your IP address** to allow access.
   - **Create a MongoDB user** and save the credentials.
   - Copy the **MongoDB URI connection string** provided.


---

## **Flask Application Structure**

The project follows a **modular structure** to separate concerns and make it easy to maintain:

```
flask_journal_app/
│── app.py                # Entry point for the Flask application
│── config.py             # Configuration for the app (includes MongoDB URI and secret key)
│── requirements.txt      # Python dependencies
│── /templates            # HTML templates for the app
│   ├── base.html         # Base template for the app
│   ├── home.html         # Template for the home page
│   ├── new_entry.html    # Template for adding a new entry
│── /journal              # The journal blueprint and models
│   ├── __init__.py       # Initialize the journal blueprint
│   ├── models.py         # Define the journal entry model
│   ├── routes.py         # Define routes for the journal
│── /extensions           # Extensions like MongoDB
│   ├── __init__.py       # MongoDB extension
│── Dockerfile            # Dockerfile to containerize the app
├── flask-journal-deployment.yaml
├── flask-journal-service.yaml
```

---

## **Dockerizing the Application**

### **1. Dockerfile**

Create a `Dockerfile` for containerization:

```Dockerfile
# Use Python 3.13.2 as base image
FROM python:3.13.2-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the Flask port
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Start the Flask application
CMD ["flask", "run"]
```

### **2. Build the Docker Image**

Build the Docker image:

```bash
docker build -t flask-journal-app .
```

### **3. Run the Docker Container**

Run the container with MongoDB URI as an environment variable:

```bash
docker run -p 5000:5000 -e MONGO_URI="your_mongodb_atlas_connection_uri" flask-journal-app
```

Now the Flask application should be accessible at `http://localhost:5000`.

---

## **Kubernetes Setup**

### **1. Kubernetes Deployment**

#### **Create Deployment and Service Manifests**

In the `kubernetes/` directory, create the following Kubernetes manifests:

#### `flask-journal-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-journal-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-journal
  template:
    metadata:
      labels:
        app: flask-journal
    spec:
      containers:
      - name: flask-journal
        image: flask-journal-app:latest
        ports:
        - containerPort: 5000
        env:
        - name: MONGO_URI
          value: "your_mongodb_atlas_connection_uri"
```

#### `flask-journal-service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-journal-service
spec:
  selector:
    app: flask-journal
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
```

### **2. Apply Kubernetes Manifests**

Apply the deployment and service manifests to your Kubernetes cluster:

```bash
kubectl apply -f kubernetes/flask-journal-deployment.yaml
kubectl apply -f kubernetes/flask-journal-service.yaml
```

---

## **Running the Application**

### **Docker**

To run the app locally using Docker:

1. Build the Docker image:  
   ```bash
   docker build -t flask-journal-app .
   ```

2. Run the container:  
   ```bash
   docker run -p 5000:5000 -e MONGO_URI="your_mongodb_atlas_connection_uri" flask-journal-app
   ```

3. Access the app at `http://localhost:5000`.

### **Kubernetes**

To deploy the app on Kubernetes:

1. Apply the Kubernetes manifests:  
   ```bash
   kubectl apply -f kubernetes/flask-journal-deployment.yaml
   kubectl apply -f kubernetes/flask-journal-service.yaml
   ```

2. Access the app via the service URL provided by Kubernetes.

---

## **Environment Variables**

The following environment variables need to be set:

- **FLASK_SECRET_KEY**: A secret key for Flask (default: `default_secret_key`).
- **MONGO_URI**: The connection string for MongoDB Atlas (required).

---
