from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig,AutoModel, AutoTokenizer
from torch import Tensor, device
import uuid
import pandas as pd
import torch
from .utils import get_relevent_table, erosion_step, augment_sql
from .models import getQueryModel, responseQueryModel
import sqlvalidator
import httpx
import asyncio

async def text_to_sql(predictQueryModel: getQueryModel) -> responseQueryModel:
    
    question= predictQueryModel.input
    user_id = predictQueryModel.user_id
    activity_id = predictQueryModel.activity_id
    database_name = predictQueryModel.database_name
    # check the schemas of the database and save the tables


    tables= "actors, finance, nba"
    headers="actors: [id, name, movie, title, genre, rating] nba: [player, team, points, championship, year] finance:[ id, amount, date ]"
    
    print("getting relevent table")

    # relevent_table = get_relevent_table( question, tables, headers )

    ## define the device to use, cuda if available else cpu
        ## this is used to run the model on GPU if available
    torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
    ## encoding model and tokenizer
    encoding_model_name = 'shahrukhx01/paraphrase-mpnet-base-v2-fuzzy-matcher'
    encoding_model = AutoModel.from_pretrained(encoding_model_name).to(torch_device)
    encoding_tokenizer = AutoTokenizer.from_pretrained(encoding_model_name)

    ## define data, we will define rows and header and column types of each column separately here
    rows = [['Lebron James', '24', 'United States', 'Center', '1999-2000', 'Barton CC (KS)'], 
            ['Shawn Respert', '31', 'United States', 'Guard', '1997-98', 'Michigan State'], 
            ['Quentin Richardson', 'N/A', 'United States', 'Forward', '2013-present', 'DePaul'], 
            ['Alvin Robertson', '7, 21', 'United States', 'Guard', '1995-96', 'Arkansas'], ['Carlos Rogers', '33, 34', 'United States', 'Forward-Center', '1995-98', 'Tennessee State'], ['Roy Rogers', '9', 'United States', 'Forward', '1998', 'Alabama'], ['Jalen Rose', '5', 'United States', 'Guard-Forward', '2003-06', 'Michigan'], ['Terrence Ross', '31', 'United States', 'Guard', '2012-present', 'Washington']]
    header = ['Player', 'No.', 'Nationality', 'Position', 'Years in Toronto', 'School/Club Team']
    header_column_types = ['text', 'text', 'text', 'text', 'text', 'text']
    
    

    # Generate the schema string with incrementing <colX> tags
    schema_parts = [
        f"<col{i}> {col} : {col_type}"
        for i, (col, col_type) in enumerate(zip(header, header_column_types))
    ]


    question_schema = question+" </s> "+ " ".join(schema_parts)

    print("Question Schema:", question_schema)
    prediction = await erosion_step(question_schema,torch_device)
    final_sql = await augment_sql(prediction, header, rows, header_column_types, question=question_schema, lookup_value=False)
    
    print("Final SQL Query:", final_sql)
    if not final_sql:
        print("No SQL query generated.")
        return None 
    sql_query = sqlvalidator.parse(final_sql)
    
    # if not sql_query.is_valid():
    #      print("Invalid SQL query generated.")
    # else:
    # If the SQL query is valid, proceed to responseQueryModel
    output = responseQueryModel(final_sql,question,user_id,activity_id,database_name)
    await predict_query(output)
    print("SQL query generated successfully:", final_sql)
    return output


# input = getQueryModel('What is the name of the player who scored the most points in the NBA?')
# output = asyncio.run(text_to_sql(input))


async def predict_query(response_model: responseQueryModel):
    """
    Makes an HTTP POST request to the /predictQuery endpoint using a responseQueryModel instance.
    """
    data = {
        "user_id": response_model.user_id,
        "activity_id": response_model.activity_id,
        "database_name": response_model.database_name,
        "input": response_model.input,
        "querypredicted": response_model.querypredicted
    }
    return data
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(
    #         "http://localhost:8000/predictQuery",
    #         json=data
    #     )
    #     response.raise_for_status()
    #     return response.json()