import os
import requests
import dlt

from datetime import datetime

# URL for the Flask mock server
MOCK_SERVER_URL = os.getenv("MOCK_SERVER_URL", "http://localhost:5000")

def fetch_all_customers():
    """Fetches all customer records from the paginated mock server."""
    customers = []
    page = 1
    limit = 50
    
    while True:
        try:
            # Fetch data from mock server
            response = requests.get(f"{MOCK_SERVER_URL}/api/customers", params={"page": page, "limit": limit})
            response.raise_for_status()
            data = response.json()
            
            # Get records from response
            records = data.get("data", [])
            if not records:
                break
            
            # Transform data types
            for record in records:
                if record.get("date_of_birth"):
                    record["date_of_birth"] = datetime.strptime(record["date_of_birth"], "%Y-%m-%d").date()
                if record.get("created_at"):
                    record["created_at"] = datetime.fromisoformat(record["created_at"].replace("Z", "+00:00"))
            
            # Add records to list
            customers.extend(records)
            
            # Check pagination metadata to see if we reached the end
            pagination = data.get("pagination", {})
            if page >= pagination.get("total_pages", 1):
                break
                
            page += 1
        except Exception as e:
            print(f"Error fetching data from mock server on page {page}: {e}")
            break
            
    return customers

@dlt.resource(
    name="customers", 
    write_disposition="merge", 
    primary_key="customer_id",
    columns={
        "date_of_birth": {"data_type": "date"},
        "created_at": {"data_type": "timestamp"},
        "account_balance": {"data_type": "decimal"}
    }
)
def customer_resource(customers_data):
    yield customers_data

def run_ingestion_pipeline():
    """Runs the dlt pipeline to ingest data into PostgreSQL."""
    customers = fetch_all_customers()
    if not customers:
        return 0

    pipeline = dlt.pipeline(
        pipeline_name="customer_ingestion",
        destination="postgres",
        dataset_name="public",
    )
    
    # Run the pipeline
    load_info = pipeline.run(customer_resource(customers))
    print(load_info)
    
    return len(customers)
