import httpx
from AI.TexttoSqlAgent.models import responseQueryModel
from AI.AnalyzersCrew.models import returnReportModel

async def returnReport(report_model: returnReportModel):
    """
    Makes an HTTP POST request to the /returnReport endpoint using a returnReportModel instance.
    """
    data = {
        "user_id": report_model.user_id,
        "activity_id": report_model.activity_id,
        "database_name": report_model.database_name,
        "input": report_model.input,
        "output": report_model.output
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/returnReport",
            json=data
        )
        response.raise_for_status()
        return response.json()
    


