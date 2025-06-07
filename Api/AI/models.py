import uuid
# create an object that holds the data to trigger the texttosql method
def str_uuid():
    return str(uuid.uuid4())

class getQueryModel(BaseModel):
    user_id:  str(uuid.uuid4())
    activity_id:  str(uuid.uuid4())
    database_name: str
    input: str
    # constructor to initialize the object with default values
    def __init__(self, **data):
        super().__init__(**data)
        self.user_id = str(uuid.uuid4())  # Generate a new UUID for user_id
        self.activity_id = str(uuid.uuid4())  # Generate a new UUID for activity_id
        self.database_name = data.get('database_name', 'default_db')  # Default database name if not provided
        self.input = data.get('input', '')  # Ensure input is set if not provided

# create an object that holds the data to trigger the texttosql method

class predictQueryModel(BaseModel):
    user_id:  str(uuid.uuid4())
    activity_id:  str(uuid.uuid4())
    database_name: str
    table_schema: dict
    input: str

# create an object to hold the Api response data 

class responseQueryModel(BaseModel):
    user_id:  str(uuid.uuid4())
    activity_id:  str(uuid.uuid4())
    database_name: str
    input: str 
    querypredicted: str
    # contructor to initialize the object with default values
    def __init__(self, **data):
        super().__init__(**data)
        self.querypredicted = "SELECT * FROM table WHERE condition"  # Default value for querypredicted
        self.input = data.get('input', '')  # Ensure input is set if not provided
        self.user_id = str(uuid.uuid4())  # Generate a new UUID for user_id
        self.activity_id = str(uuid.uuid4())  # Generate a new UUID for activity_id
        self.database_name = data.get('database_name', 'default_db')  # Default database name if not provided

