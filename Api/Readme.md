All new features and fixes are to be pushed to api-integration-bart until integration is ready.

## API Gateway (main.py)

- **/process** (POST): Integrates Text-to-SQL service (port 8001) and SQL Tools service (port 8002)
    - **expects:**  
      ```json
      {
        "user_input": "<natural language query>",
        "user_id": "<string>"
      }
      ```
    - **returns:**  
      ```json
      {
        "sql": "<generated_sql_query>",
        "result": "<query_result_data>"
      }
      ```
- **Environment variables:**  
    - `PREDICT_SQL_URL` (default: `http://localhost:8001/predict_sql`)
    - `SQLTOOLS_URL` (default: `http://localhost:8002/run_query`)

## How to run API Gateway locally

1. Go to the Api directory:
cd Api

2. Install dependencies:
pip install -r requirements.txt

3. Create a `.env` file with:
USE_MOCKS=true
PREDICT_SQL_URL=http://localhost:8001/predict_sql
SQLTOOLS_URL=http://localhost:8002/run_query

*(set `USE_MOCKS=false` to use real services later)*

4. Start the server:
uvicorn main:app --reload --host 0.0.0.0 --port 8000

5. Open in browser or test via API:  
[http://localhost:8000/docs](http://localhost:8000/docs)
