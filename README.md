# CDR (Call Detail Records) Microservices Application

## Overview

The CDR application is a robust microservices-based system designed for processing, storing, analyzing, and visualizing call detail records. It comprises three core microservices:

1. **MS-Loader**: A Python service for parsing and loading CDR files into the database.
2. **MS-Backend**: A Spring Boot service for data processing and API endpoints.
3. **MS-Frontend**: A React-based UI for visualizing call analytics.

---

## Architecture

![CDR Microservices Architecture](https://placeholder-for-architecture-diagram.com)

### Microservices Overview

- **MS-Loader**: 
    - Parses CDR files (CSV, JSON, XML).
    - Validates and stores records in PostgreSQL.
    - Publishes events to Kafka for downstream processing.

- **MS-Backend**: 
    - Consumes Kafka messages.
    - Processes data and provides REST APIs for analytics.

- **MS-Frontend**: 
    - React-based UI with Keycloak authentication.
    - Visualizes CDR data through interactive dashboards.

---

## Key Features

- **Multi-format file parsing**: Supports CSV, JSON, XML, and YAML.
- **Real-time data processing**: Powered by Kafka.
- **Advanced analytics**: Multi-dimensional insights (e.g., by day, service type, source, destination).
- **Interactive visualizations**: Charts and reports.
- **Secure authentication**: Integrated with Keycloak.
- **Kubernetes-ready**: Seamless deployment on Kubernetes clusters.

---

## Services

### MS-Loader

A Python-based service responsible for:
- Parsing and validating CDR files.
- Transforming and storing data in PostgreSQL.
- Publishing records to Kafka for further processing.

**Tech Stack**: Python, PostgreSQL, Kafka, Docker.

---

### MS-Backend

A Java Spring Boot service responsible for:
- Consuming and processing CDR records from Kafka.
- Providing REST APIs for analytics and reporting.
- Managing authentication and authorization.

**Tech Stack**: Java, Spring Boot, MySQL, Kafka, Keycloak, Docker.

---

### MS-Frontend

A React-based UI responsible for:
- User authentication via Keycloak.
- Visualizing data with interactive charts.
- Providing a call analytics dashboard and report generation.

**Tech Stack**: React, TypeScript, Vite, Keycloak, Docker.

---

## Deployment

The system is designed for Kubernetes deployment with the following components:

1. **Databases**:
     - PostgreSQL for MS-Loader.
     - MySQL for MS-Backend.

2. **Message Queue**:
     - Kafka cluster for inter-service communication.

3. **Authentication**:
     - Keycloak for identity and access management.

4. **Services**:
     - MS-Loader, MS-Backend, and MS-Frontend.

---

## Getting Started

### Prerequisites

- Docker and Docker Compose.
- Kubernetes cluster (e.g., Minikube for local development).
- Kafka.
- PostgreSQL/MySQL.
- Keycloak.

### Environment Configuration

Each service has its own configuration parameters. Refer to the individual service documentation for details:

- [MS-Loader Configuration](https://github.com/Basma-90/Callnsights/tree/main/ms-loader/docs)
- [MS-Backend Configuration](https://github.com/Basma-90/Callnsights/blob/main/ms-backend/demo/README.md)
- [MS-Frontend Configuration](https://github.com/Basma-90/Callnsights/blob/main/ms-frontend/README.md)