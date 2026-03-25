# mock-pipe
The technical assessment built with two different frameworks (FastAPI and Flask).

This project consists of two main services:
- **Mock Server (Flask)**: Serves mock customer data.
- **Pipeline Service (FastAPI)**: Ingests the data from the mock server and stores it in a PostgreSQL database.

## Prerequisites
- Docker and Docker Compose (for containerized setup)
- Python 3.11+ (for manual setup)
- PostgreSQL (if running Pipeline Service manually)

---

## Running with Docker Compose (Recommended)

The easiest way to run the entire stack (Mock Server, Pipeline Service, and PostgreSQL) is using Docker Compose.

1. Ensure Docker is running.
2. From the project root directory, execute:
   ```bash
   docker-compose up -d --build
   ```
3. The services will be available at:
   - **Mock Server**: `http://localhost:5000`
   - **Pipeline Service**: `http://localhost:8000`
   - **PostgreSQL**: `localhost:5432` (User: `postgresql`, Password: `admin`, DB: `customer_db`)

---

## Running Manually (Without Docker)

You can also run the services individually on your local machine.

### 1. Running the Mock Server (Flask)

1. Navigate to the `mock-server` directory:
   ```bash
   cd mock-server
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .venv/Scripts/activate
   # On macOS/Linux:
   # source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask application:
   ```bash
   flask run
   ```
   *(Runs at `http://127.0.0.1:5000`)*

### 2. Running the Pipeline Service (FastAPI)

1. Navigate to the `pipeline-service` directory:
   ```bash
   cd pipeline-service
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .venv/Scripts/activate
   # On macOS/Linux:
   # source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure you have a local PostgreSQL instance running. Set the required environment variables (in Windows PowerShell, use `$env:VAR_NAME="value"`):
   ```powershell
   # If your database credentials differ from the default:
   $env:DATABASE_URL="postgresql://postgres:admin@localhost:5432/customer_db"
   
   # Point to the running Mock Server:
   $env:MOCK_SERVER_URL="http://localhost:5000"
   ```
5. Run the FastAPI application:
   ```bash
   fastapi dev main.py
   # Or using Uvicorn directly:
   # uvicorn main:app --reload
   ```
   *(Runs at `http://127.0.0.1:8000`)*

---

Risyandi - 2026