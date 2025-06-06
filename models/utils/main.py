from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


def get_relevent_table(question, tables, headers):
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
    return response['text'].strip()  # Assuming the response is a dictionary with 'text' key

tables= "actors, finance, nba"
headers="actors: [id, name, movie, title, genre, rating] nba: [player, team, points, championship, year] finance:[ id, amount, date ]"
question= "What is numbers of players that have scored more than 30 points in a game?"

relevent_table = get_relevent_table(question, tables, headers)

print(relevent_table)  


