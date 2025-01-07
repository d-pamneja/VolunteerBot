from ..dependencies import *
from .prompts import *
from src.question_query.utils import *

# Tool for question based query
def question_query_tool(user_query: str) -> str:
    try:
        return get_final_response_question_query(user_query)
    except Exception as e:
        return f"Error processing question query: {str(e)}"
    
# Tools for the chatbot
tools = [
    Tool(
        name="questionQuery",
        func=question_query_tool,
        description="Use for fetching information from relevant documents."
    )
]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm=ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")

# Initializing the Agent
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True,
    memory=memory,
    agent_kwargs={
        'prefix': template.format(custom_instructions=custom_instructions, input='{input}', agent_scratchpad='{agent_scratchpad}'),
    }
)