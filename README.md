# Project Tracker - Private Cloud Deployment
**B8IS003 Cloud Infrastructure & Virtualisation**  
**Assessment 2 (40%)**

## Overview
A fully containerised project-tracking web application deployed on a private cloud infrastructure (simulated OpenStack compute node). The solution meets all enterprise requirements for data sensitivity and on-premise hosting.

## Tech Stack
- Flask + SQLAlchemy + Bootstrap 5
- SQLite (persistent)
- Docker

## Quick Start (Docker)
```
docker build -t project-tracker . --no-cache
mkdir -p data
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/data:/data \
  --name project-tracker-app \
  project-tracker
```


### 2. Oral Defence Cheat Sheet (10-15 min Q&A with Paul Laird)

Print this or keep it open during the session. These are the **most likely questions** based on the assignment brief.

**Expected Questions & Model Answers**

```
1. **Why did you choose a private cloud instead of a public cloud?**  
   → “Because the scenario explicitly requires data sensitivity and regulatory compliance.
 A private cloud guarantees full data residency on-premise,
 which public clouds cannot provide without additional legal agreements.”
```
```
2. **Why OpenStack?**  
   → “OpenStack is the leading open-source IaaS platform. It gives complete control over compute, storage and networking, and it natively supports Docker containers – exactly what the assignment asked for.”
```
```
3. **Why Docker for containerisation?**  
   → “Docker provides portability, lightweight resource usage, and easy versioning. It also makes deployment consistent between development and the private cloud environment.”
```
```
4. **Explain your volume mount strategy.**  
   → “We mounted only the `/data` directory (`-v $(pwd)/data:/data`) so the SQLite database persists across container restarts. Mounting the entire `/app` folder caused issues earlier, so we corrected it to avoid overwriting application files.”
```
```
5. **How is networking configured?**  
   → “The application is only exposed on the internal private network (192.168.100.0/24). No floating IP or public access – exactly as required for data sensitivity.”
```
```
6. **What challenges did you face?**  
   → “The biggest challenge was the volume mount overwriting files. We solved it by changing the mount point and updating the database URI to an absolute path inside the volume.”
```
```
7. **How would you scale this in production?**  
   → “We would use OpenStack Magnum to deploy Kubernetes for orchestration, add persistent storage with Cinder, and implement proper logging/monitoring with Prometheus.”
```
```
8. **How did you test the application?**  
   → “We performed full CRUD testing – add, view, edit and delete projects – both locally and inside the Docker container. Screenshots in the report show the working application.”
```
```
9. **What is the role of the persistent volume?**  
   → “It ensures the projects.db file survives if the container is stopped or restarted – critical for a stateful application.”
```
```
10. **Any final reflection?**  
    → “This project showed me how powerful the combination of private cloud + containers is for secure, compliant workloads. I now understand why volume management and networking are so important in real deployments.”
```
