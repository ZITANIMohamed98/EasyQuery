from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig,AutoModel, AutoTokenizer
from torch import Tensor, device
import uuid
import pandas as pd
import torch


tables= "actors, finance, nba"
headers="actors: [id, name, movie, title, genre, rating] nba: [player, team, points, championship, year] finance:[ id, amount, date ]"
question= "What is numbers of players that have scored more than 30 points in a game?"

relevent_table = get_relevent_table(question, tables, headers)

## define the device to use, cuda if available else cpu
    ## this is used to run the model on GPU if available
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
## encoding model and tokenizer
encoding_model_name = 'shahrukhx01/paraphrase-mpnet-base-v2-fuzzy-matcher'
encoding_model = AutoModel.from_pretrained(encoding_model_name).to(torch_device)
encoding_tokenizer = AutoTokenizer.from_pretrained(encoding_model_name)

## define data, we will define rows and header and column types of each column separately here
rows = [['Aleksandar Radojević', '25', 'Serbia', 'Center', '1999-2000', 'Barton CC (KS)'], ['Shawn Respert', '31', 'United States', 'Guard', '1997-98', 'Michigan State'], ['Quentin Richardson', 'N/A', 'United States', 'Forward', '2013-present', 'DePaul'], ['Alvin Robertson', '7, 21', 'United States', 'Guard', '1995-96', 'Arkansas'], ['Carlos Rogers', '33, 34', 'United States', 'Forward-Center', '1995-98', 'Tennessee State'], ['Roy Rogers', '9', 'United States', 'Forward', '1998', 'Alabama'], ['Jalen Rose', '5', 'United States', 'Guard-Forward', '2003-06', 'Michigan'], ['Terrence Ross', '31', 'United States', 'Guard', '2012-present', 'Washington']]
header = ['Player', 'No.', 'Nationality', 'Position', 'Years in Toronto', 'School/Club Team']
header_column_types = ['text', 'text', 'text', 'text', 'text', 'text']

question_schema = """What is aleksander's  nationality? 
                        </s> <col0> Player : text <col1> No. : text <col2> Nationality : text 
                        <col3> Position : text <col4> Years in Toronto : text <col5>  School/Club Team : text"""

prediction = erosion_step(question_schema)
final_sql, _, _, _, _ = augment_sql(prediction, header, rows, header_column_types, question=question_schema, lookup_value=False)
print(final_sql)



