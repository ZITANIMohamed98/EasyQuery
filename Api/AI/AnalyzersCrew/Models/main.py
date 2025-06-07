
# create an object to hold the Api request to execute the query

class executeQueryModel(BaseModel):
    user_id:  str(uuid.uuid4())
    activity_id:  str(uuid.uuid4())
    database_name: str
    input: str
    
# create an object to hold the Api response data after executing the query

class returnReportModel(BaseModel):
    user_id:  str(uuid.uuid4())
    activity_id:  str(uuid.uuid4())
    database_name: str
    input: str
    output: str 