# NIM AI Assistant Setup Guide

## Prerequisites

- Docker and Docker Compose
- NVIDIA GPU with CUDA support
- NVIDIA Container Toolkit

## Setup Steps

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/nim-ai-assistant.git
   cd nim-ai-assistant
   ```

2. Configure the application:
   - Update `config/nim_config.yaml` with your desired settings
   - Update `config/model_config.yaml` if necessary

3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

4. Access the application:
   - API: http://localhost:8000
   - Prometheus metrics: http://localhost:9090
   - Grafana dashboard: http://localhost:3000

## Running Tests

To run the tests, use the following command:

```
docker-compose run nim-ai-assistant pytest
```

## Monitoring

The application exposes Prometheus metrics on port 9090. You can configure Grafana to visualize these metrics by setting up a Prometheus data source and creating dashboards.
