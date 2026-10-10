# Assignment 2 — College ERP DevOps Pipeline

**Student:** Shrutika Mane | **Roll No.:** 24107135  
**Repository:** https://github.com/24107135-sudo/college-erp-devops-assignment-2

## Q1 — CI/CD, Docker and Compose

The GitHub Actions workflow runs the API unit tests, validates Docker Compose, builds the application containers, trains the model, deploys the services, and smoke-tests the API, Prometheus, and Grafana. Docker Compose runs the Flask API, MLflow, Prometheus, and Grafana. Service ports are 8000, 5000, 9090, and 3000 respectively.

## Q2 — ML lifecycle and monitoring

`train_model.py` creates a reproducible student performance regression model, logs parameters and MAE to MLflow, and registers `StudentPerformancePredictor` version 1. `app.py` serves score predictions from the registered model and exposes prediction counters and latency metrics. Prometheus scrapes `/metrics`; the provisioned Grafana dashboard displays prediction rate and p95 latency.

## Q3 — End-to-end pipeline

The [architecture diagram and run instructions](./ARCHITECTURE.md) show the Agile planning, Git branching and review, automated CI, container build, Compose deployment, MLflow tracking/model registry, and Prometheus/Grafana monitoring.

### Evidence

- Repository: https://github.com/24107135-sudo/college-erp-devops-assignment-2
- GitHub Actions: https://github.com/24107135-sudo/college-erp-devops-assignment-2/actions

Capture screenshots of the successful GitHub Actions job and the MLflow/Grafana interfaces as execution evidence. Docker was not available on the authoring workstation; Compose is configured to run in GitHub-hosted CI.
