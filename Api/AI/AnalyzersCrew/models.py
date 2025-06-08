import uuid
import pandas as pd
# create an object to hold the Api request to execute the query

class executeQueryModel:
    
    def __init__(self, user_id=None, activity_id=None, database_name='default_db', input=''):
        self.user_id = user_id if user_id else str(uuid.uuid4())  # Generate a new UUID for user_id if not provided
        self.activity_id = activity_id if activity_id else str(uuid.uuid4())  # Generate a new UUID for activity_id if not provided
        self.database_name = database_name  # Use provided database name or default to 'default_db'    
        self.input = input  # Use provided input or default to an empty string 
    
# create an object to hold the Api response data after executing the query

class returnReportModel:
    def __init__(self, user_id=None, activity_id=None, database_name='', input='', output=''):
        self.user_id = user_id if user_id else str(uuid.uuid4())  # Generate a new UUID for user_id if not provided
        self.activity_id = activity_id if activity_id else str(uuid.uuid4())  # Generate a new UUID for activity_id if not provided
        self.data= pd.DataFrame  # Use provided database name or default to 'default_db'
        self.input = input  # Use provided input or default to an empty string
        self.output = output  # Use provided output or default to an empty string