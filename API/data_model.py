from .dependencies import *

# Data Models for Input and Output

# Query Schemas
class GetRelevantDocs(BaseModel):
    query : str = Field(...,description="The text string which has to be converted to an embedding")
    
class RelevantText(BaseModel):
    score: float = Field(..., description="The similarity score of the record")
    text: str = Field(..., description="The content of the relevant text chunk")
    reference: int = Field(..., description="The page number where the chunk is located (1-indexed)")

class RelevantTextsList(BaseModel):
    texts: List[RelevantText] = Field(..., description="A list of relevant text objects with scores and references")
 
class GetResponse(BaseModel):
    user_query : str = Field(...,description="The text string which is passed as a query to the LLM")
    
class Response(BaseModel):
    response : str = Field(...,description="The final response given by the LLM of the user query")
    
# Chatbot Schemas
class ChatInput(BaseModel):
    user_query: str = Field(...,description="The text string which has to be converted to an embedding")

class ChatResponse(BaseModel):
    response: str = Field(...,description="The text string which is passed as a query to the LLM")
    conversation_history: List[str] = Field(...,description="The conversation history of the chatbot")