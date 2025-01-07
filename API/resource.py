# Importing the dependencies
from .dependencies import *
from src.chatbot.utils import *
from src.dependencies import *
from src.question_query.utils import *
from src.question_query.prompts import *
from .data_model import *

# Initialising the API from FastAPI and APIRouter
app = FastAPI(prefix="/aimind")
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return "Hello from Volunteer Bot!"

@app.post("/aimind/chat", response_model=ChatResponse)
async def chat(input: ChatInput):
    """
    Endpoint for real-time chat interaction with the agent.
    """
    try:
        # Process the initial query
        user_query = str(input.user_query)
        logging.info(f"User query: {user_query}")
        response = agent.run(user_query)
        
        # Fetch the conversation history
        chat_history = memory.load_memory_variables({})["chat_history"]
        
        # Format the conversation history for display
        formatted_history = [
            f"User: {msg.content}" if isinstance(msg, HumanMessage) else f"Chatbot: {msg.content}"
            for msg in chat_history
        ]
        
        return ChatResponse(response=response, conversation_history=formatted_history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the query: {e}")
