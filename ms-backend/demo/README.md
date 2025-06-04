# MS-Backend Service Documentation

## Overview

MS-Backend is a Spring Boot microservice designed to process Call Detail Records (CDR) data from Kafka, store it in a MySQL database, and provide REST APIs for data retrieval and analysis. It is part of a larger CDR processing system, which includes:
- **MS-Loader**: For loading CDR files.
- **MS-Frontend**: For visualization.

---

## Technology Stack

- **Java**: JDK 21  
- **Framework**: Spring Boot  
- **Database**: MySQL  
- **Message Broker**: Kafka  
- **Authentication**: Keycloak (OAuth2/OIDC)  
- **Containerization**: Docker  
- **Orchestration**: Kubernetes  

---

## API Documentation

### Base URL
`/api/cdrs`

### Authentication
All endpoints under `/api/v1/**` require a valid JWT token with the `USER` role from Keycloak.

### Endpoints

#### 1. Get All CDRs
- **Method**: `GET /api/cdrs`  
- **Description**: Retrieves all CDR records.  
- **Response**:  
    - `200 OK`: Array of CDR objects.

#### 2. Get CDR by ID
- **Method**: `GET /api/cdrs/{id}`  
- **Description**: Retrieves a specific CDR record by its ID.  
- **Parameters**:  
    - `id` (Long): The ID of the CDR record.  
- **Responses**:  
    - `200 OK`: CDR object.  
    - `404 Not Found`: CDR not found.

#### 3. Create CDR
- **Method**: `POST /api/cdrs`  
- **Description**: Creates a new CDR record.  
- **Request Body**: CDR object.  
- **Response**:  
    - `200 OK`: Created CDR object with ID.

#### 4. Update CDR
- **Method**: `POST /api/cdrs/update`  
- **Description**: Updates an existing CDR record.  
- **Request Body**: CDR object with ID.  
- **Responses**:  
    - `200 OK`: Updated CDR object.  
    - `400 Bad Request`: Invalid request (e.g., CDR ID not found).

#### 5. Delete CDR
- **Method**: `DELETE /api/cdrs/{id}`  
- **Description**: Deletes a CDR record.  
- **Parameters**:  
    - `id` (Long): The ID of the CDR record to delete.  
- **Response**:  
    - `204 No Content`.

#### 6. Get CDRs by Source
- **Method**: `GET /api/cdrs/source?source={sourceValue}`  
- **Description**: Retrieves CDR records matching the specified source.  
- **Query Parameters**:  
    - `source` (String): The source value to filter by.  
- **Responses**:  
    - `200 OK`: Array of CDR objects.  
    - `404 Not Found`: No CDRs found for the source.

#### 7. Get CDRs by Service Type
- **Method**: `GET /api/cdrs/service-type?serviceType={serviceTypeValue}`  
- **Description**: Retrieves CDR records matching the specified service type.  
- **Query Parameters**:  
    - `serviceType` (String): Service type (VOICE, SMS, DATA).  
- **Responses**:  
    - `200 OK`: Array of CDR objects.  
    - `404 Not Found`: No CDRs found for the service type.

#### 8. Get CDRs by Usage Range
- **Method**: `GET /api/cdrs/usage-range?minUsage={min}&maxUsage={max}`  
- **Description**: Retrieves CDR records with usage values between the specified range.  
- **Query Parameters**:  
    - `minUsage` (Double): Minimum usage value.  
    - `maxUsage` (Double): Maximum usage value.  
- **Responses**:  
    - `200 OK`: Array of CDR objects.  
    - `404 Not Found`: No CDRs found in the usage range.

#### 9. Get Aggregated CDRs
- **Method**: `GET /api/cdrs/aggregated?groupBy={groupByType}&serviceType={serviceType}&startDate={startDate}&endDate={endDate}`  
- **Description**: Retrieves aggregated CDR data based on various criteria.  
- **Query Parameters**:  
    - `groupBy` (String): Grouping type (`day`, `service`, `source`, `destination`).  
    - `serviceType` (String, optional): Filter by service type.  
    - `startDate` (String, optional): Start date (ISO format).  
    - `endDate` (String, optional): End date (ISO format).  
- **Responses**:  
    - `200 OK`: Aggregated data.  
    - `400 Bad Request`: Invalid groupBy parameter.  
    - `500 Internal Server Error`: Error processing request.

#### 10. Health Check
- **Method**: `GET /api/cdrs/health`  
- **Description**: Checks if the service is running.  
- **Response**:  
    - `200 OK`: `"Cdr Service is running"`.

#### 11. Home Endpoint
- **Method**: `GET /api/v1/home`  
- **Description**: Returns information about the authenticated user.  
- **Responses**:  
    - `200 OK`: JSON with user details.  
    - `401 Unauthorized`: `{"message": "Unauthorized"}`.

---

## Model Classes

### CDR
| Field         | Type            | Description                                 |
|---------------|-----------------|---------------------------------------------|
| `id`          | Long            | Unique identifier.                         |
| `source`      | String          | Source phone number or identifier.         |
| `destination` | String          | Destination phone number or identifier.    |
| `startTime`   | LocalDateTime   | Start time of the call/message/session.    |
| `serviceType` | ServiceType     | Type of service (VOICE, SMS, DATA).        |
| `usage`       | Double          | Usage amount (duration, data volume, etc.).|
| `fileName`    | String          | Name of the file the record came from.     |

---

## Kafka Integration

- **Topic**: `cdr-records`  
- **Consumer Group**: `new-consumer-group-2025`  
- **Message Format**: JSON object representing a CDR record.

---

## Security

- **Authentication**: Keycloak (OAuth 2.0 Resource Server with JWT validation).  

---

## Setup Instructions

### Prerequisites
1. JDK 21  
2. Maven  
3. MySQL  
4. Kafka  
5. Keycloak  

### Local Development Setup
1. **Clone the repository**:  
     ```bash
     git clone <repository-url>
     cd ms-backend/demo
     ```
2. **Configure MySQL**:  
     ```sql
     CREATE DATABASE cdr_db;
     CREATE USER 'cdr_user'@'%' IDENTIFIED BY 'cdr_password';
     GRANT ALL PRIVILEGES ON cdr_db.* TO 'cdr_user'@'%';
     FLUSH PRIVILEGES;
     ```
3. **Configure Keycloak**:  
     - Set up a realm named `cdr-platform`.  
     - Create a client named `ms-backend` with client authentication enabled.  
     - Create a role named `USER` and assign it to a test user.  

4. **Run the application**:  
     ```bash
     mvn clean package
     java -jar target/demo-0.0.1-SNAPSHOT.jar
     ```

---

## Docker and Kubernetes

### Docker
1. **Build Docker image**:  
     ```bash
     docker build -t ms-backend:latest .
     ```
2. **Run with Docker**:  
     ```bash
     docker run -p 5500:5500 \
     -e SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/cdr_db?allowPublicKeyRetrieval=true&useSSL=false \
     -e SPRING_DATASOURCE_USERNAME=cdr_user \
     -e SPRING_DATASOURCE_PASSWORD=cdr_password \
     -e SPRING_KAFKA_BOOTSTRAP_SERVERS=kafka:29092 \
     ms-backend:latest
     ```

### Kubernetes
1. **Deploy MySQL**:  
     ```bash
     kubectl apply -f db-deployment.yaml
     kubectl apply -f mysql-configMap.yaml
     kubectl apply -f mysql-secrets.yaml
     ```
2. **Deploy MS-Backend**:  
     ```bash
     kubectl apply -f ms-backend-deployment.yaml
     kubectl apply -f ms-backend-service.yaml
     ```
3. **Verify Deployment**:  
     ```bash
     kubectl get pods
     kubectl get services
     ```

---

## Configuration Reference

### `application.yaml`
Key configuration options:
```yaml
server:
  port: 5500

spring:
  application:
    name: ms-backend

  datasource:
    url: jdbc:mysql://localhost:3306/cdr_db?allowPublicKeyRetrieval=true&useSSL=false
    username: root
    password: password
  
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQLDialect

  kafka:
    bootstrap-servers: localhost:29092
    consumer:
      group-id: new-consumer-group-2025
      auto-offset-reset: earliest
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.apache.kafka.common.serialization.StringDeserializer
    listener:
      concurrency: 3

  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: http://localhost:8081/realms/cdr-platform
          jwk-set-uri: http://localhost:8081/realms/cdr-platform/protocol/openid-connect/certs
      client:
        registration:
          keycloak:
            client-id: ms-backend
            client-secret: BHZg91EL04cQYs6Ianz3naBQTrszK3cB
            authorization-grant-type: client_credentials

  web:
     cors:
      allowed-origins: "http://localhost:5173,http://127.0.0.1:5173,*"
      allowed-methods: "GET, POST, PUT, DELETE, OPTIONS"
      allowed-headers: "*"
      allow-credentials: true
      exposed-headers: "Authorization, Content-Type, X-Requested-With"
      max-age: 3600

keycloak:
  admin-url: http://localhost:8081/admin/realms/
  realm: cdr-platform
  client-id: ms-backend
  client-secret: BHZg91EL04cQYs6Ianz3naBQTrszK3cB
```

