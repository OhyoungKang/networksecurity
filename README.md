# Network Security Project – Phishing Detection System

## Overview:

This project implements an end-to-end machine learning pipeline for phishing website detection.
It covers the full lifecycle from data ingestion and model training to experiment tracking, containerized deployment, and automated CI/CD on AWS.

The system is designed using production-style MLOps practices, focusing on reproducibility, automation, and scalable deployment.

## Key Features
	•	Machine learning-based phishing URL classification
	•	Experiment tracking using MLflow
	•	Dataset versioning with DagsHub
	•	REST inference API built with FastAPI
	•	Docker-based containerized deployment
	•	Automated CI/CD pipeline via GitHub Actions
	•	Secure container registry using AWS ECR
	•	Automated runtime deployment on AWS EC2 (self-hosted runner)

## System Architecture

Inference Flow:

User → FastAPI → ML Model → Prediction

CI/CD Flow:

GitHub Push
→ GitHub Actions pipeline
→ Docker image build
→ Push image to AWS ECR
→ EC2 self-hosted runner pulls latest image
→ Container redeployed automatically


## Tech Stack

Machine Learning
	•	Python
	•	Scikit-learn
	•	Pandas
	•	NumPy

MLOps / Experiment Tracking
	•	MLflow
	•	DagsHub

API Layer
	•	FastAPI
	•	Uvicorn

DevOps / Cloud
	•	Docker
	•	GitHub Actions
	•	AWS ECR
	•	AWS EC2

## Health Endpoints (Monitoring)

The service exposes multiple health endpoints for runtime monitoring and deployment validation.

• GET /health  
Basic service status check

• GET /health/live  
Liveness probe — verifies that the API process is running

• GET /health/ready  
Readiness probe — checks MongoDB connectivity and service dependencies

• GET /health/system  
System resource monitoring (CPU, memory, disk usage)

## Deployment Pipeline
	1.	Code pushed to the main branch
	2.	GitHub Actions builds a Docker image
	3.	The image is pushed to AWS ECR
	4.	EC2 self-hosted runner pulls the latest image
	5.	Existing container is replaced with the new deployment

## Author

Ohyoung Kang
AI / MLOps Engineer