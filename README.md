# lambda-patentes-aws

### Challenge 

Develop a serverless system that processes license plate readings and determines which advertising campaign applies based on a set of basic rules (location, time window, and max exposures per plate). Two APIs are required: one for processing readings and storing exposure results, and another for consulting metrics.


## Deployment Instructions

### Local Testing:

 - Install Python dependencies `pip install -r requirements.txt` and similarly for metrics if needed).
 - Initialize the SQLite database: `sqlite3 db.db < db/schema.sql 2>error.log` .
 - Test each Lambda function locally using provided Python commands.

### Deployment to AWS:
- Package your Lambda functions (create zip files).
- Run terraform init and terraform apply to provision AWS resources.
- Update environment variables if switching from SQLite to PostgreSQL.


## API Usage Examples

- Process Reading API:
 - Endpoint: POST /process
  - Body:
  ```
        {
            "reading _ id": "read123",
            "timestamp": "2025-03-04T10:00:00",
            "license _ plate": "ABC123",
            "checkpoint _ id": "CHECK_01",
            "location": {
                "latitude": 40.7128,
                "longitude": -74.0060
            }
        }
    ```


## Metrics API:
- Endpoint: GET /metrics
- Response: JSON with totals per checkpoint, totals per campaign, and latest exposures. 

Assumptions & Decisions

The campaign rules are hardcoded for simplicity.
SQLite is used for local testing; in production, a PostgreSQL RDS instance should be used.
Error handling is basic; further improvements may include more robust validations and logging.
The Terraform configuration is minimal and serves as a starting point for real AWS deployment.
Architecture Diagram
Include the diagram provided above or embed an image generated from your favorite diagram tool.


### testing locally 

For local testing, you can simulate API Gateway events by passing a JSON event to your handlers. For example:

Testing Process Reading API:

```
python3 -c "import json; from lambda_functions.process_reading.handler import lambda_handler; event = {\"body\": json.dumps({\"reading_id\": \"read123\", \"timestamp\": \"2025-03-04T10:00:00\", \"license_plate\": \"ABC123\", \"checkpoint_id\": \"CHECK_01\", \"location\": {\"latitude\": 40.7128, \"longitude\": -74.0060}})}; print(lambda_handler(event))"

```

metrics
```
python3 -c "from lambda_functions.metrics.handler import lambda_handler; print(lambda_handler({}))"

```