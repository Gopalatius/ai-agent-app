import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load environment variables from .env file
load_dotenv()

# Retrieve Google API key for Gemini from environment variables
# IMPORTANT: Replace "YOUR_GOOGLE_API_KEY" with your actual key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY")

def get_llm_response(prompt: str) -> str:
    """
    Generates a response to a general or open-ended question using the Gemini LLM.

    Args:
        prompt (str): The question or prompt for the LLM.

    Returns:
        str: The LLM's generated response, or an error message.
    """
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY":
        return "Google API key not configured for LLM. Please set GOOGLE_API_KEY in your environment."

    try:
        # Initialize the ChatGoogleGenerativeAI model
        # Using "gemini-2.5-flash", with temperature 0 for more deterministic answers
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0)
        
        # Invoke the LLM with the human message
        response = llm.invoke([HumanMessage(content=prompt)])
        
        # Return the content of the LLM's response
        return response.content
    except Exception as e:
        # Catch any errors during LLM invocation
        return f"Error getting LLM response: {e}"