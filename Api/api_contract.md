## API Contracts

### Gateway expects from other services:

- **predict_sql()**
  - URL: `/predict_sql` (default port: 8001)
  - Method: POST
  - Input:
    ```json
    {
      "user_id": "...",
      "activity_id": "...",
      "database_name": "...",
      "input": "..."
    }
    ```
  - Output:
    ```json
    {
      "sql": "..."
    }
    ```

- **run_query (SQL Tools)**
  - URL: `/run_query` (default port: 8002)
  - Method: POST
  - Input:
    ```json
    {
      "user_id": "...",
      "activity_id": "...",
      "database_name": "...",
      "input": "...",
      "query": "..."
    }
    ```
  - Output:
    ```json
    {
      "data": [...]
    }
    ```

- **Frontend connects to:**  
  - `/getQuery` (port 8000)
  - `/executeQuery` (port 8000)
  - `/process` (legacy, port 8000)

- **Mock mode:**  
  - set `USE_MOCKS=true` in `.env` for local tests without services

### Ports
- API Gateway: 8000
- predict_sql: 8001
- SQLTools: 8002
