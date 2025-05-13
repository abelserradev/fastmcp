# Integration Seguros Mercantil - Developer Guidelines

This document provides essential information for developers working on the Integration Seguros Mercantil project.

## Build/Configuration Instructions

### Local Development Setup

1. **Environment Setup**:
   - Python 3.12 is required
   - The project uses `uv` for dependency management

2. **Install Dependencies**:
   ```bash
   uv sync --frozen --no-cache
   ```

3. **Environment Variables**:
   - Copy `.env.local` to `.env` for local development
   - For staging, use `.env.stage`
   - For production, use `.env.prod`

4. **Run the Application**:
   ```bash
   python run.py
   ```
   - The application will run on port 9000 by default
   - In development mode, the application will reload automatically when code changes

### Docker Setup

1. **Build and Run with Docker Compose**:
   ```bash
   docker compose up --build
   ```

2. **Environment-Specific Configurations**:
   - For development: `docker compose -f docker-compose_test.yml up --build`
   - For staging: `docker compose -f docker-compose_staging.yml up --build`
   - For production: `docker compose -f docker-compose.yml up --build`

## Testing Information

### Setting Up Testing Environment

1. **Install Testing Dependencies**:
   ```bash
   uv pip install pytest httpx
   ```

2. **Test Directory Structure**:
   - Place test files in the `tests/` directory
   - Name test files with the prefix `test_` (e.g., `test_api.py`)
   - Name test functions with the prefix `test_` (e.g., `test_api_health()`)

### Running Tests

1. **Run All Tests**:
   ```bash
   python -m pytest
   ```

2. **Run Specific Test File**:
   ```bash
   python -m pytest tests/test_api.py
   ```

3. **Run with Verbosity**:
   ```bash
   python -m pytest -v
   ```

### Creating New Tests

1. **Example Test**:
   ```python
   import pytest
   from fastapi.testclient import TestClient
   from app.api.app import app

   client = TestClient(app)

   def test_example():
       response = client.get("/health")
       assert response.status_code == 200
       assert response.json() == {"status": "ok"}
   ```

2. **Testing API Endpoints**:
   - Use the FastAPI TestClient to make requests to your API
   - For endpoints requiring authentication, include the API key in the request headers
   - Example:
     ```python
     def test_authenticated_endpoint():
         headers = {"X-API-Key": "test_api_key"}
         response = client.get("/protected-endpoint", headers=headers)
         assert response.status_code == 200
     ```

## Additional Development Information

### Project Structure

- `app/api/`: Contains the API routes and endpoints
  - Organized by version (v1, v2, v3, v4)
  - Each version has its own modules (Integration_SM, PasarelaPagoMS)
- `app/schemas/`: Contains Pydantic models for request/response validation
- `app/middlewares/`: Contains middleware components
- `app/utils/`: Contains utility functions and constants

### Code Style and Conventions

1. **Docstrings**:
   - Use docstrings for all functions, classes, and modules
   - Include parameter descriptions and return types
   - Example:
     ```python
     def function_name(param1, param2):
         """
         Brief description of the function.
         
         Args:
             param1: Description of param1
             param2: Description of param2
             
         Returns:
             Description of the return value
         """
     ```

2. **Error Handling**:
   - Use try/except blocks for error handling
   - Log errors with appropriate level (error, warning, info)
   - Raise HTTPException with appropriate status code and detail message

3. **Logging**:
   - Use the logger from `app.utils.v1.LoggerSingleton`
   - Log important events with appropriate level

### CI/CD Pipeline

- The project uses Bitbucket Pipelines for CI/CD
- Different branches deploy to different environments:
  - `develop` branch deploys to the development environment
  - `staging` branch deploys to the staging environment
  - `main` branch deploys to the production environment

### API Documentation

- API documentation is available at `/docs` when the application is running
- The documentation is generated automatically from the code