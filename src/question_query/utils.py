from ..dependencies import *
from ..logger import *
from .prompts import *

def get_embedding(text) :
    """
        Function to convert the text string into embeddings using text-embedding-3-small from OpenAI
    
        Args:
            text : A string which will contain either the text chunk or the user query
            
        Returns:
            vector : A vector of 1536 dimensions
    """
    
    try:
        response = embedding_model.create(
            input=text,
            model="text-embedding-3-small"
        )
        
        return response.data[0].embedding   
    
    except Exception as e:
        raise CustomException(e,sys)
    
def get_relevant_chunks(query,index):
    """
        Function to find the most relevant documents from the vectorDB and return the text chunks, it's cosine score and page number
    
        Args:
            query : A string the user query
            index : The instance of the index to search from
            
        Returns:
            vectors : A final collection of relevant data in the format : 
                1. score : The cosine similarity score of the record with the user query
                2. text : The text chunk of the relevant document
                3. reference : The page number where this chunk is located
    """
    query_vector = get_embedding(query)
    
    results = index.query(
        vector = query_vector,
        top_k = 3,
        include_values = False,
        include_metadata = True,
    )
    
    logging.info(f"Results fetched from the vectorDB from the index : {PINECONE_INDEX_NAME}")
    
    relevant_texts = []
    for record in results['matches']:
        text = {}
        text['score'] = record['score']
        text['text'] = record['metadata']['chunk']
        text["reference"] = int(record["metadata"]["page_number"]) + 1
        relevant_texts.append(text)
        
    logging.info(f"Relevant documents in desired format fetched for the query : {query}")
    
    return relevant_texts

# Prompt Template Instance
query_prompt = PromptTemplate(
    input_variables=["query","documents"],
    template=query_prompt_template
)

# Langchain Instances
chat = ChatOpenAI(
    temperature = 0,  
    model = "gpt-4o",
    openai_api_key = OPENAI_API_KEY
)

query_chain = chat | (lambda x: x)

def get_final_response_question_query(user_query) : 
    """
        Function to get the final answer from the LLM
    
        Args:
            user_query : A string the user query
            
        Returns:
            text : A final string which gives the response of the query from the document
    """
    
    docs = get_relevant_chunks(user_query,index)
    logging.info(docs)
    
    formatted_prompt = query_prompt.format(query=user_query, documents=str(docs))
    response = query_chain.invoke(formatted_prompt)

    logging.info(f"Final response generated from the LLM : {response.content}")
    return response.content