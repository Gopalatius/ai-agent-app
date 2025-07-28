import os
import json
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from langchain_core.agents import AgentAction, AgentFinish


# Import custom tools
from app.tools.weather import get_weather
from app.tools.math_tool import evaluate_math_expression
from app.tools.llm_tool import get_llm_response

# Load environment variables
load_dotenv()

# Retrieve Google API key for the agent's reasoning LLM
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY")

# Initialize the LLM that the LangChain agent will use for its reasoning process
# Using "gemini-2.5-flash" with temperature 0 for more focused decision-making.
llm_for_agent = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0)

# Define the tools that the LangChain agent can use.
# Each tool is defined using `Tool.from_function` for simplicity,
# providing a name, the function to call, and a clear description.
# The description is crucial for the LLM to understand when to use each tool.

weather_tool = Tool.from_function(
    func=get_weather,
    name="WeatherTool",
    description="Fetches current weather information for a given location. Input should be a string representing the location, e.g., 'London' or 'Paris'. Use this tool when the user asks about weather or climate."
)

math_tool = Tool.from_function(
    func=evaluate_math_expression,
    name="MathTool",
    description="Performs a basic math operation on a simple arithmetic expression. Input should be a string representing a simple expression like '42 * 7', '10 + 5', '20 / 4'. Use this tool when the user asks for a calculation."
)

llm_tool = Tool.from_function(
    func=get_llm_response,
    name="LLMTool",
    description="Answers general or open-ended questions using a language model. Use this tool for any question that is not specifically about weather or math, or when other tools cannot answer."
)

# List of all tools available to the agent
tools = [weather_tool, math_tool, llm_tool]

# Define the prompt template for the ReAct agent.
# This prompt guides the LLM on how to reason, select tools, and format its output.
prompt_template = PromptTemplate.from_template("""
You are a helpful AI assistant that can route user queries to the appropriate tool.
You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
""")

# Create the ReAct agent using the LLM, tools, and prompt.
agent = create_react_agent(llm_for_agent, tools, prompt_template)

# Create the AgentExecutor, which is responsible for running the agent's logic.
# `verbose=True` prints the agent's thought process to the console (useful for debugging).
# `handle_parsing_errors=True` helps the agent recover from minor parsing issues.
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

def process_query_with_agent_streaming(query: str):
    """
    Processes a user query using the LangChain agent and streams the final result.
    It identifies the tool used during the agent's execution.

    Args:
        query (str): The natural language query from the user.

    Yields:
        str: A JSON string containing the original query, the tool used, and the result.
    """
    tool_used = "llm" # Default to 'llm' if no specific tool action is observed
    final_result = "An unexpected error occurred or no response from agent."
    tool_identified = False # Flag to ensure we only capture the first tool used

    print(f"--- Starting process_query_with_agent_streaming for query: {query} ---")

    try:
        # Iterate over the synchronous generator provided by agent_executor.stream()
        for chunk in agent_executor.stream({"input": query}):
            print(f"Received chunk: {chunk}") # Log each chunk received

            # Check for 'actions' key to identify tool usage
            if "actions" in chunk and isinstance(chunk["actions"], list) and len(chunk["actions"]) > 0:
                agent_action = chunk["actions"][0]
                if not tool_identified and isinstance(agent_action, AgentAction):
                    tool_used_raw = agent_action.tool
                    if tool_used_raw == "WeatherTool":
                        tool_used = "weather"
                    elif tool_used_raw == "MathTool":
                        tool_used = "math"
                    elif tool_used_raw == "LLMTool":
                        tool_used = "llm"
                    tool_identified = True
                    print(f"Tool identified: {tool_used} from 'actions' chunk.")

            # Check for 'output' key for the final result
            if "output" in chunk:
                final_result = chunk["output"]
                print(f"Final result captured from 'output' chunk: {final_result}")
                # Once the final output is received, we have the conclusive answer.
                break # Exit the loop as we have the result.

            # Also check for 'agent' key if it contains AgentFinish (for robustness, though 'output' is more direct)
            if "agent" in chunk and isinstance(chunk["agent"], AgentFinish):
                final_result = chunk["agent"].return_values["output"]
                print(f"Final result captured from 'agent' (AgentFinish) chunk: {final_result}")
                break # Exit the loop.

    except Exception as e:
        final_result = f"An error occurred during agent execution: {e}"
        tool_used = "llm" # Fallback to LLM if agent fails
        print(f"Exception caught: {e}") # Log the exception

    print(f"--- Yielding result: tool_used={tool_used}, final_result={final_result} ---")
    # Yield the complete structured JSON response after the loop has finished
    # and final_result and tool_used have been determined.
    # Adding a newline character (`\n`) makes it compatible with line-delimited JSON streaming.
    yield json.dumps({
        "query": query,
        "tool_used": tool_used,
        "result": final_result
    }) + "\n"