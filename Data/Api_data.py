

# create an object to hold the Api request data {userId, activityId, Table schema, input}
query_request_data = {
    "userId": str(uuid.uuid4()),
    "activityId": str(uuid.uuid4()),
    "tableSchema": "",
    "input": ""
}


# create an object to hold the Api response data {userId, activityId, Table schema, output}
query_response_data = {
    "userId": api_request_data["userId"],
    "activityId": api_request_data["activityId"],
    "tableSchema": api_request_data["tableSchema"],
    "output": ""
}   


