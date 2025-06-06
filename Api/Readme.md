"All new features and fixes are to be pushed to api-integration-bart until integration is ready."

## API Gateway (main.py)

- **/getQuery** (POST): Gets a SQL query for a natural language input
    - expects:
      ```json
      {
        "user_id": "user42",
        "activity_id": "hack2024",
        "database_name": "trips",
        "input": "Show all completed trips in Seattle"
      }
      ```
    - returns:
      ```json
      {
        "user_id": "user42",
        "activity_id": "hack2024",
        "database_name": "trips",
        "query": "SELECT * FROM trips WHERE city='Seattle' AND status='completed'"
      }
      ```
- **/executeQuery** (POST): Executes a SQL query and returns results
    - expects:
      ```json
      {
        "user_id": "user42",
        "activity_id": "hack2024",
        "database_name": "trips",
        "input": "Show all completed trips in Seattle",
        "query": "SELECT * FROM trips WHERE city='Seattle' AND status='completed'"
      }
      ```
    - returns:
      ```json
      {
        "user_id": "user42",
        "activity_id": "hack2024",
        "database_name": "trips",
        "query": "SELECT * FROM trips WHERE city='Seattle' AND status='completed'",
        "data": [{"trip_id": 123, "city": "Seattle", "database": "trips"}]
      }
      ```
- **/process** (POST): (legacy endpoint, kept for backward compatibility)

- **Environment variables:**  
    - `PREDICT_SQL_URL` (default: `http://localhost:8001/predict_sql`)
    - `SQLTOOLS_URL` (default: `http://localhost:8002/run_query`)
    - `USE_MOCKS` (default: `false`)

## How to run API Gateway locally

1. Go to the Api directory:
```bash
cd Api
