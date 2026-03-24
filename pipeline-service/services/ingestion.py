import os
import requests
import dlt

# URL for the Flask mock server
MOCK_SERVER_URL = os.getenv("MOCK_SERVER_URL", "http://localhost:5000")

def fetch_all_customers():
    """Fetches all customer records from the paginated mock server."""
    customers = []
    page = 1
    limit = 50
    
    while True:
        try:
            response = requests.get(f"{MOCK_SERVER_URL}/api/customers", params={"page": page, "limit": limit})
            response.raise_for_status()
            data = response.json()
            
            records = data.get("data", [])
            if not records:
                break
            
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

@dlt.resource(name="customers", write_disposition="merge", primary_key="customer_id")
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
