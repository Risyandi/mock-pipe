import os
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

def load_customers():
    """Load mock customer data from JSON file."""
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'customers.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Data file not found at {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in {file_path}")
        return []

# Load data into memory on startup
CUSTOMERS = load_customers()

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

# Get all customers endpoint
@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Paginated list of customers."""
    # Parse pagination parameters (default to page 1, limit 10)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    # Ensure positive integers for pagination
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10
        
    # Calculate slice indices
    start_idx = int((page - 1) * limit)
    end_idx = int(start_idx + limit)
    
    paginated_data = CUSTOMERS[start_idx:end_idx]
    
    return jsonify({
        "data": paginated_data,
        "total": len(CUSTOMERS),
        "page": page,
        "limit": limit
    }), 200

# Get a single customer by ID endpoint
@app.route('/api/customers/<id>', methods=['GET'])
def get_customer(id):
    """Get a single customer by ID."""
    # Assuming the ID matches the 'customer_id' field in JSON
    customer = next((c for c in CUSTOMERS if c.get('customer_id') == id), None)
    
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
        
    return jsonify(customer), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
