from pydantic import BaseModel, Field
from typing import Literal, Union

class QueryRequest(BaseModel):
    """
    Pydantic model for the incoming query request.
    """
    query: str = Field(..., example="What's the weather today in Paris?")

class QueryResponse(BaseModel):
    """
    Pydantic model for the structured JSON response.
    """
    query: str
    tool_used: Literal["weather", "math", "llm"]
    result: Union[str, float, int] # Result can be string (weather, llm) or number (math)