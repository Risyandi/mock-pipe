import os
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import engine, Base, get_db
from models.customer import Customer
from services.ingestion import run_ingestion_pipeline

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pipeline Service")

# Ingest data from mock server to PostgreSQL endpoint
@app.post("/api/ingest")
def ingest_data():
    """Endpoint to trigger data ingestion from the mock server to PostgreSQL."""
    try:
        # For dlt postgres destination we pass credentials through environment variable
        db_url = os.getenv("DATABASE_URL", "postgresql://postgres:admin@localhost:5432/customer_db")
        os.environ["DESTINATION__POSTGRES__CREDENTIALS"] = db_url

        records_processed = run_ingestion_pipeline()
        return {"status": "success", "records_processed": records_processed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get all customers endpoint
@app.get("/api/customers")
def get_customers(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    """Retrieve paginated results from the database."""
    offset = (page - 1) * limit
    customers = db.query(Customer).offset(offset).limit(limit).all()
    total_records = db.query(func.count(Customer.customer_id)).scalar()
    total_pages = 0 if total_records == 0 else (total_records + limit - 1) // limit
    
    return {
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages,
        "data": customers
    }

# Get single customer by id endpoint
@app.get("/api/customers/{id}")
def get_customer(id: str, db: Session = Depends(get_db)):
    """Return single customer or 404."""
    customer = db.query(Customer).filter(Customer.customer_id == id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# Health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
