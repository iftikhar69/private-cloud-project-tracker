# Project Tracker - Private Cloud Deployment

## Overview
A fully containerised project-tracking web application deployed on a private cloud infrastructure (simulated OpenStack compute node). The solution meets all enterprise requirements for data sensitivity and on-premise hosting.

## Tech Stack
- Flask + SQLAlchemy + Bootstrap 5
- SQLite (persistent)
- Docker

## Quick Start (Docker)

 step 1 
Make sure you have installed:
Docker
check: 
```
docker --version
```
 step 2 Build Docker Image
Run this inside the project directory:

```
docker build -t project-tracker .
---
```
step 3 Run Container

```
docker run -d -p 5000:5000 -v "$(pwd)/data:/data" --name project-tracker-app project-tracker
```
Access Application

Open your browser and go to:

http://localhost:5000

