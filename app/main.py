from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.models import QueryRequest, QueryResponse
from app.agent import process_query_with_agent_streaming # Import the streaming agent function
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the FastAPI application
app = FastAPI(
    title="AI Agent Router API",
    description="A small backend app that routes natural language commands to specific tools (Weather, Math, LLM).",
    version="1.0.0"
)

# Root endpoint for basic health check
@app.get("/")
async def root():
    """
    Root endpoint to confirm the API is running.
    """
    return {"message": "AI Agent Router API is running!"}

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Accepts a user query via a POST request and routes it to the appropriate tool.
    
    The LangChain agent determines which tool (Weather, Math, or LLM) to use.
    The response is streamed, providing a structured JSON output once the tool execution is complete.

    Args:
        request (QueryRequest): The incoming request containing the user's query.

    Returns:
        StreamingResponse: A streaming response containing the structured JSON result.
    """
    # FastAPI's StreamingResponse expects an async generator or an iterator.
    # Our `process_query_with_agent_streaming` function is an async generator
    # that yields a single, complete JSON string once the agent's processing is done.
    # The `media_type="application/json"` indicates that the content is JSON.
    return StreamingResponse(process_query_with_agent_streaming(request.query), media_type="application/json")
