# Pipeline Service

A FastAPI-based REST API that ingests customer data from the mock server and performs an upsert operation into a PostgreSQL database.

## Prerequisites

- Python 3.11+ (or compatible version)
- `pip` package manager
- PostgreSQL database
- (Optional) Docker, if you wish to run the service in a container

## Local Setup

Follow these steps to set up and run the pipeline service locally on your machine.

### 1. Create a Virtual Environment

It is highly recommended to use a Python virtual environment to manage dependencies locally.
Run the following command from the `pipeline-service` directory to create a virtual environment named `.venv`:

```bash
# On Windows
python -m venv .venv

# On macOS/Linux
python3 -m venv .venv
```

### 2. Activate the Virtual Environment

Before installing dependencies, you need to activate the virtual environment:

```bash
# On Windows (Command Prompt)
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

*Note: You'll know it's activated when you see `(.venv)` at the beginning of your terminal prompt.*

### 3. Install Dependencies

Once the virtual environment is activated, install the required Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Ensure you have a running PostgreSQL database. You can configure the database URL via the `DATABASE_URL` environment variable. The default connection string is:
`postgresql://postgres:admin@localhost:5432/customer_db`

### 5. Run the Server

Start the FastAPI application by running `main.py` with `uvicorn` (or `fastapi dev`):

```bash
fastapi dev  # Or: uvicorn main:app --reload
```

The server should now be running locally at `http://127.0.0.1:8000/` or `http://localhost:8000/`.

---

## Running with Docker

If you prefer to run the pipeline service using Docker, the `Dockerfile` is already configured for you.

### 1. Build the Docker Image

From the `pipeline-service` directory, run:

```bash
docker build -t pipeline-service .
```

### 2. Run the Docker Container

Start the container and map port 8000 to your local machine. Don't forget to pass the `DATABASE_URL` environment variable if your database is not accessible via the default local connection:

```bash
docker run -p 8000:8000 -e DATABASE_URL=postgresql://postgres:admin@host.docker.internal:5432/customer_db pipeline-service
```

The server will be available at `http://localhost:8000/`.

---

## API Endpoints

The pipeline service provides the following endpoints:

### POST `/api/ingest`
Endpoint to trigger data ingestion from the mock server to PostgreSQL.
- **Response**: `{"status": "success", "records_processed": <count>}` (200 OK)

### GET `/api/customers`
Retrieve paginated results from the database.
- **Query Parameters**:
  - `page` (integer, default: 1): The specific page number.
  - `limit` (integer, default: 20): Number of records per page (up to 100).
- **Example**: `GET /api/customers?page=2&limit=10`
- **Response**: JSON object containing `data` (list of customers), `total_records`, `total_pages`, `page`, and `limit`.

### GET `/api/customers/<id>`
Return details for a single customer by their `customer_id`.
- **Example**: `GET /api/customers/CUST-001`
- **Response**: Details of the requested customer, or `404 Not Found` if the customer does not exist.

## Data Destination

The pipeline service performs upsert operations on a PostgreSQL database table named `customers`. It utilizes the `dlt` (data load tool) library to manage the robust ingestion pipeline.
