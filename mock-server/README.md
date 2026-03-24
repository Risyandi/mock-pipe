# Mock Server

A simple Flask-based mock REST API that serves customer data from a static JSON file.

## Prerequisites

- Python 3.12+ (or compatible version)
- `pip` package manager
- (Optional) Docker, if you wish to run the server in a container

## Local Setup

Follow these steps to set up and run the mock server locally on your machine.

### 1. Create a Virtual Environment

It is highly recommended to use a Python virtual environment to manage dependencies locally.
Run the following command from the `mock-server` directory to create a virtual environment named `.venv`:

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
.venv/Scripts/activate

# On macOS/Linux
source .venv/bin/activate
```

*Note: You'll know it's activated when you see `(.venv)` at the beginning of your terminal prompt.*

### 3. Install Dependencies

Once the virtual environment is activated, install the required Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Run the Server

Start the Flask application by running `app.py`:

```bash
python app.py or flask run
```

The server should now be running locally at `http://127.0.0.1:5000/` or `http://localhost:5000/`.

---

## Running with Docker

If you prefer to run the mock server using Docker, the `Dockerfile` is already configured for you.

### 1. Build the Docker Image

From the `mock-server` directory, run:

```bash
docker build -t mock-server .
```

### 2. Run the Docker Container

Start the container and map port 5000 to your local machine:

```bash
docker run -p 5000:5000 mock-server
```

The server will be available at `http://localhost:5000/`.

---

## API Endpoints

The mock server provides the following endpoints:

### GET `/api/health`
Health check endpoint to verify the server is running.
- **Response**: `{"status": "healthy"}` (200 OK)

### GET `/api/customers`
Returns a paginated list of customers from `data/customers.json`.
- **Query Parameters**:
  - `page` (integer, default: 1): The specific page number.
  - `limit` (integer, default: 10): Number of records per page.
- **Example**: `GET /api/customers?page=2&limit=5`
- **Response**: JSON object containing `data` (list of customers), `total` count, `page`, and `limit`.

### GET `/api/customers/<id>`
Returns details for a single customer by their `customer_id`.
- **Example**: `GET /api/customers/CUST-001`
- **Response**: Details of the requested customer, or `404 Not Found` if the customer does not exist.

## Data Source

The mock server loads its data from `data/customers.json` on startup. If this file is missing or contains invalid JSON, the server will log a warning and return empty sets.
