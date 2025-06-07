import uuid

class getQueryModel:
  
    # constructor to initialize the object with default values
    def __init__(self, user_id=None, activity_id=None, database_name='default_db', input=''):
        self.user_id = user_id if user_id else str(uuid.uuid4())  # Generate a new UUID for user_id if not provided
        self.activity_id = activity_id if activity_id else str(uuid.uuid4())  # Generate a new UUID for activity_id if not provided
        self.database_name = database_name  # Use provided database name or default to 'default_db'
        self.input = input  # Use provided input or default to an empty string



# create an object that holds the data to trigger the texttosql method

class listAllowedDbModel:

    def __init__(self, user_id=None, database_list= []):
        self.user_id = user_id if user_id else str(uuid.uuid4())
        self.data

# create an object to hold the Api response data 

class responseQueryModel:
    # contructor to initialize the object with default values
    def __init__(self, **data):
        super().__init__(**data)
        self.querypredicted = "SELECT * FROM table WHERE condition"  # Default value for querypredicted
        self.input = data.get('input', '')  # Ensure input is set if not provided
        self.user_id = str(uuid.uuid4())  # Generate a new UUID for user_id
        self.activity_id = str(uuid.uuid4())  # Generate a new UUID for activity_id
        self.database_name = data.get('database_name', 'default_db')  # Default database name if not provided

