## API Contracts

### Gateway expects from other services:

- **predict_sql()**
  - URL: `/predict_sql` (default port: 8001)
  - Method: POST
  - Input: `{"user_input": "...", "user_id": "..."}`
  - Output: `{"sql": "..."}`

- **run_query (SQL Tools)**
  - URL: `/run_query` (default port: 8002)
  - Method: POST
  - Input: `{"query": "...", "user_id": "..."}`
  - Output: `{"data": [...]}`

- **Frontend connects to:**  
  - `/process` (port 8000)

- **Mock mode:**  
  - set `USE_MOCKS=true` in `.env` for local tests without services

### Ports
- API Gateway: 8000
- predict_sql: 8001
- SQLTools: 8002
