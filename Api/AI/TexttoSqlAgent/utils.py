from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig,AutoModel, AutoTokenizer
from torch import Tensor, device
import uuid
import pandas as pd
import torch

torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
encoding_model_name = 'shahrukhx01/paraphrase-mpnet-base-v2-fuzzy-matcher'
encoding_model = AutoModel.from_pretrained(encoding_model_name).to(torch_device)
encoding_tokenizer = AutoTokenizer.from_pretrained(encoding_model_name)
async def get_relevent_table(question, tables, headers):
    """
    Returns the relevant table and its headers based on the question.
    
    Args:
        question (str): The question to be answered.
        tables (str): A comma-separated string of table names.
        headers (str): A comma-separated string of headers for each table.

    Returns:
        str: The name of the relevant table and its headers.
    """
    # This function is a placeholder for the actual implementation
    # that would determine the relevant table based on the question.
    template = """Question: return only the name of the relevent table that we need to query to get the data for this question{question} knowing that the list of tables of the database {tables}, with the headers {headers}

    Answer: select only by the relevent table and its headers, do not return any other information, just the table name and its headers"""

    prompt = ChatPromptTemplate.from_template(template)

    model = OllamaLLM(model="llama3")

    chain = prompt | model

    response = chain.invoke({"tables": tables, "headers": headers, "question": question})
    if isinstance(response, dict) and 'text' in response:
        return response['text'].strip()
    elif isinstance(response, str):
        return response.strip()
    else:
        raise ValueError("Unexpected response type from chain.invoke")


# define the erosion step function
# this function takes a question schema as input and generates a SQL query using a pre-trained BART model

async def erosion_step(question_schema, torch_device):
    """This function is used to genrate the SQL query from the question and table schema
    It uses a pre-trained BART model to generate the SQL query.
    """
    
    ## define the model hub's model name
    model_name = "shahrukhx01/schema-aware-denoising-bart-large-cnn-text2sql"

    ## load model and tokenizer
    model = BartForConditionalGeneration.from_pretrained('shahrukhx01/schema-aware-denoising-bart-large-cnn-text2sql').to(torch_device)
    tokenizer = BartTokenizer.from_pretrained('shahrukhx01/schema-aware-denoising-bart-large-cnn-text2sql')

    # prepare question, this is how the table header looks like for this example
    ##['Player', 'No.', 'Nationality', 'Position', 'Years in Toronto', 'School/Club Team']

    ## we have to encode schema and concat the question alonside it as follows
    ## tokenize question_schema
    inputs = tokenizer([question_schema], max_length=1024, return_tensors='pt').to(torch_device)

    # generate SQL
    text_query_ids = model.generate(inputs['input_ids'], num_beams=4, min_length=0, max_length=125, early_stopping=True)
    prediction = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in text_query_ids][0]

    return(prediction)



## define the helper functions below
async def cos_sim(a: Tensor, b: Tensor):
    """
    borrowed from sentence transformers repo
    Computes the cosine similarity cos_sim(a[i], b[j]) for all i and j.
    :return: Matrix with res[i][j]  = cos_sim(a[i], b[j])
    """
    if not isinstance(a, torch.Tensor):
        a = torch.tensor(a)

    if not isinstance(b, torch.Tensor):
        b = torch.tensor(b)

    if len(a.shape) == 1:
        a = a.unsqueeze(0)

    if len(b.shape) == 1:
        b = b.unsqueeze(0)

    a_norm = torch.nn.functional.normalize(a, p=2, dim=1)
    b_norm = torch.nn.functional.normalize(b, p=2, dim=1)
    return torch.mm(a_norm, b_norm.transpose(0, 1))


#Mean Pooling - Take attention mask into account for correct averaging
async def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

## get embedding of a word
async def get_embedding(value):
    value = value.lower()
    value = [" ".join([x for x in value])]
    # Tokenize sentences
    encoded_input = encoding_tokenizer(value, padding=True, truncation=True, return_tensors='pt').to(torch_device)

    # Compute token embeddings
    with torch.no_grad():
        model_output = encoding_model(**encoded_input)

    # Perform pooling. In this case, max pooling.
    embedding = await mean_pooling(model_output, encoded_input['attention_mask'])
    return embedding

## encodes categorical data into vector space
async def encode_data(data, header, header_types):
    table = pd.DataFrame(data, columns=header)
    data = {}
    #cell = " ".join([x for x in generated_data])
    for header_val, header_type_val in zip(header, header_types):
        encoded_vals = Tensor().to(torch_device)
        if header_type_val == 'text':
            for value in table[header_val]:
                #encoded_vals.append()
                emb = await get_embedding(value)
                encoded_vals  = torch.cat((encoded_vals, emb), 0)
        data[header_val] = encoded_vals.cpu()
    return data, table

## external memory lookup
async def memory_lookup(embeddings, query_value, column_values, lookup_map, column_map, cond_col, threshold=1.0):
    lookup_value = None
    query_value = query_value.replace('`','').strip()
    sorted_sim, index = await compute_cosine(query_value, embeddings)
    if sorted_sim >= .70:
        lookup_value = column_values[index]
    else:
        for col in list(lookup_map.keys()):
            embeddings = lookup_map[col]
            sorted_sim, index = compute_cosine(query_value, embeddings)
            if sorted_sim >= .95:
                lookup_value = column_map[col].vlaues[index]
                cond_col = col
            break
    return (cond_col, lookup_value)

## compute cosine similarity between matrix of candidattes and a query vector      
async def compute_cosine(query_value, embeddings):
    query_embedding = await get_embedding(query_value)
    query_embedding = query_embedding.to(torch_device)
    embeddings = embeddings.to(torch_device)

    sim = await cos_sim(embeddings, query_embedding)
    sorted_sim, indices = torch.sort(sim, axis=0, descending=True)
    return sorted_sim[0][0].item(), indices[0][0].item()

## define sql augment function to resolved the ambigous entities
sql_operators = ['>', '=', '<', '>=', '<=', '<>']
agg_operators = ['MAX', 'AVG', 'MIN', 'COUNT', 'SUM']
async def augment_sql(sql, header, rows, header_types, question, lookup_value=False):
    header = header
    rows = rows
    header_types = header_types
    encoded_data, table = await encode_data(rows, header, header_types)
    
    try:
        select_clause = sql.split('FROM')[0].strip().split('SELECT')[1]
        agg_clause = [agg_operator for agg_operator in agg_operators if agg_operator in select_clause]
        select_cols = [column for idx,column in enumerate(header) if f"<col{idx}>" in select_clause]
        where_clause = []
        where_conditions = []
        if 'WHERE' in sql:
            where_clause = sql.split('WHERE')[1].split('AND')
            for condition in where_clause:
                column = [(column, f"<col{idx}>") for idx,column in enumerate(header) if f"<col{idx}>" in condition]
                operator = None
                if len(column):
                    condition = condition.replace(column[0][1],column[0][0])
                    for op in sql_operators:
                        if op in condition:
                            operator = op
                else:
                    break
               
                if len(column) and operator:
                    cond_col, operator, con_val = column[0][0], operator, condition.split(operator)[1]
                    cond_col_type = header_types[header.index(cond_col)]
                    if operator == '=' and cond_col_type == 'text':
                        if not lookup_value:
                            cond_col, lookup_value = await memory_lookup(
                                embeddings=encoded_data[cond_col], 
                                query_value=con_val, 
                                column_values=table[cond_col].values ,
                                lookup_map= encoded_data,
                                column_map=table,
                                cond_col=cond_col,
                                threshold=1.0
                            )
                        else: 
                            lookup_value = con_val.replace('`','').strip()
                        if lookup_value:
                            where_conditions.append(f"{cond_col} {operator} \'{lookup_value}\'")
                    elif operator in ['>', '<', '>=', '<=', '<>'] and cond_col_type == 'real':
                        con_val = con_val.replace('`','').strip()
                        not_number = True
                        for x in con_val:
                            if x.isdigit() or x == '.':
                                continue
                            else:
                                not_number = False
                        if not_number and con_val in question:
                            where_conditions.append(f"{cond_col} {operator} \'{con_val}\'")
                        
            
    except Exception as e:
        print('error parsing sql', e)
        return None, None
    where_final = " AND ".join(where_conditions)
    agg_final = ""
    if len(agg_clause):
        agg_final = agg_clause[0]
    select_final = f"SELECT {agg_final} "+ " , ".join(select_cols)
    table_name = str(uuid.uuid4())
    sql_final = f"{select_final} FROM table "
    if len(where_conditions):
        sql_final += f"WHERE {where_final} "
    return (sql_final)
 


def read_training_data():
    df = pd.read_parquet('train-00000-of-00001.parquet')

    print(df.head())
