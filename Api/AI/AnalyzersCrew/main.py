from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig,AutoModel, AutoTokenizer
from torch import Tensor, device
import uuid
import pandas as pd
import torch




# from Api.AI.AnalyzersCrew.Crew import test

# print ("Loading text_to_sql function...")

# def text_to_sql() -> str:
#     """
#     Convert a natural language question into an SQL query based on the provided table schema.

#     Args:
#         question (str): The natural language question to convert.
#         tables (str): A string containing the names of the tables involved in the query.
#         headers (str): A string containing the headers of the tables.

#     Returns:
#         str: The generated SQL query.
#     """
    # question = ModelInput.input
    # tables = ModelInput.database_name  # Assuming this is a string with table names
    # headers = "col0, col1, col2, col3, col4, col5"  # Example headers, adjust as needed
    # relevent_table = get_relevent_table(question, tables, headers)

    # ## define the device to use, cuda if available else cpu
    # ## this is used to run the model on GPU if available
    # torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # ## encoding model and tokenizer
    # encoding_model_name = 'shahrukhx01/paraphrase-mpnet-base-v2-fuzzy-matcher'
    # encoding_model = AutoModel.from_pretrained(encoding_model_name).to(torch_device)
    # encoding_tokenizer = AutoTokenizer.from_pretrained(encoding_model_name)

    # ## define data, we will define rows and header and column types of each column separately here
    # rows = relevent_table['rows']
    # header = relevent_table['header']
    # header_column_types = relevent_table['header_column_types']

    # question_schema = f"{question} </s> <col0> {header[0]} : {header_column_types[0]} <col1> {header[1]} : {header_column_types[1]} <col2> {header[2]} : {header_column_types[2]} <col3> {header[3]} : {header_column_types[3]} <col4> {header[4]} : {header_column_types[4]} <col5> {header[5]} : {header_column_types[5]}"

    # prediction = erosion_step(question_schema)
    
    # final_sql, _, _, _, _ = augment_sql(prediction, header, rows, header_column_types, question=question_schema, lookup_value=False)
    
    # return final_sql


