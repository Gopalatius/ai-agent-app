# AI Agent Router Application

This project implements a small backend HTTP API that acts as an AI agent router. It accepts natural language commands, intelligently routes them to the correct "tool" for processing using LangChain, and returns a structured JSON response with the result of that tool's execution. This application simulates the core of an AI agent architecture in a simplified, accessible way, suitable for an AI engineering job application.

## Features

* **FastAPI Backend**: A robust and high-performance web framework.
* **LangChain Integration**: Utilizes LangChain for intelligent routing of user queries to appropriate tools.
* **Tool-Based Architecture**:
  * **Weather Tool**: Fetches real-time weather data using the OpenWeatherMap API.
  * **Math Tool**: Performs basic arithmetic operations safely.
  * **LLM Tool**: Answers general or open-ended questions using the Google Gemini API.
* **Structured JSON Responses**: Consistent output format for all tool executions.
* **Streaming Endpoint**: The `/query` endpoint is implemented as a streaming endpoint.
* **Dockerized**: Easily containerize and deploy the application.
* **Best Practices**: Follows good coding practices for structure, security, and maintainability.

## Deliverables

* `app/`: Source code for the FastAPI application, including tool implementations and LangChain agent logic.
* `Dockerfile`: For containerizing the application.
* `requirements.txt`: Python dependencies.
* `README.md`: This document, providing setup, run instructions, and API examples.

## Setup and Run Instructions

### Prerequisites

* Python 3.10+
* pip (Python package installer)
* Docker (if you plan to run it via Docker)

### 1. Clone the Repository


```bash
git clone https://github.com/Gopalatius/ai-agent-app.git
```

### 2. Set Up Environment Variables

This application requires API keys for OpenWeatherMap and Google Gemini. Make sure to make .env file in the root directory.

#### OpenWeatherMap API Key:

1. Go to [OpenWeatherMap](https://openweathermap.org/) and sign up for a free account.
2. Generate an API key.
3. Add this key to a `.env` file in the root directory of your project (e.g., `ai-agent-app/.env`):

```env
OPENWEATHER_API_KEY="YOUR_OPENWEATHER_API_KEY_HERE"
```

#### Google Gemini API Key:

1. Go to [Google AI Studio](https://aistudio.google.com/) and generate an API key.
2. Add this key to the same `.env` file:

```env
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
```

Your `.env` file should look like this:

```env
OPENWEATHER_API_KEY="your_open_weather_map_api_key"
GOOGLE_API_KEY="your_google_gemini_api_key"
```

### 3. Install Dependencies (if running locally)

Navigate to the root directory of your project (where `requirements.txt` is located) and install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

You have two options to run the application: locally or using Docker.

#### Option 1: Run Locally

From the root directory of your project, run the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

* `app.main:app`: Specifies that Uvicorn should run the app instance from the `main.py` file inside the app directory.
* `--host 0.0.0.0`: Makes the server accessible from all network interfaces.
* `--port 8000`: Runs the application on port 8000.
* `--reload`: (Optional) Reloads the server automatically on code changes (useful for development).

The application will be accessible at `http://localhost:8000`.

#### Option 2: Run with Docker

**Build the Docker Image:**

Navigate to the root directory of your project (where `Dockerfile` is located) and build the Docker image:

```bash
docker build -t ai-agent-router .
```

**Run the Docker Container:**

Once the image is built, run the container, mapping port 8000 from the container to port 8000 on your host machine:

```bash
docker run -p 8000:8000 --env-file .env ai-agent-router
```

* The `--env-file .env` flag tells Docker to load your API keys from the `.env` file into the container's environment.

The application will be accessible at `http://localhost:8000`.

## API Endpoint

The application exposes a single POST endpoint:

### `POST /query`

**Description**: Accepts a natural language query and routes it to the appropriate tool (Weather, Math, or LLM) for processing.

**Request Body (JSON)**:

```json
{
  "query": "What's the weather today?"
}
```

**Response Body (JSON - streamed as a single chunk)**:

The response will be a structured JSON object, indicating the original query, the tool used, and the result of the tool's execution.

```json
{
  "query": "What's the weather like today in Paris?",
  "tool_used": "weather",
  "result": "It's 20.37°C and few clouds in Paris, FR."
}
```

## Sample Input/Output Examples

You can test the API using tools like `curl`, Postman, or by writing a simple Python script.

### Example 1: Weather Query

**Input**:

```json
{
  "query": "What's the weather like today in Paris?"
}
```

**curl Command**:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What's the weather like today in Paris?\"}"
```

**Expected Output**:

```json
{
  "query": "What's the weather like today in Paris?",
  "tool_used": "weather",
  "result": "It's 20.37°C and few clouds in Paris, FR."
}
```

*(Note: Temperature and description may vary based on real-time weather data.)*

### Example 2: Math Query

**Input**:

```json
{
  "query": "What's 42 * 6?"
}
```

**curl Command**:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What's 42 * 6?\"}"
```

**Expected Output**:

```json
{
  "query": "What's 42 * 6?",
  "tool_used": "math",
  "result": "252"
}
```

### Example 3: LLM Query

**Input**:

```json
{
  "query": "Who is the president of France?"
}
```

**curl Command**:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Who is the president of France?\"}"
```

**Expected Output**:

```json
{
  "query": "Who is the president of France?",
  "tool_used": "llm",
  "result": "The current president of France is Emmanuel Macron."
}
```

*(Note: LLM responses can vary slightly.)*

## Code Structure

```
ai-agent-app/
├── app/
│   ├── __init__.py         # Initializes the app package
│   ├── main.py             # FastAPI application entry point
│   ├── models.py           # Pydantic models for request and response
│   ├── agent.py            # LangChain agent definition and routing logic
│   └── tools/              # Directory for individual tool implementations
│       ├── __init__.py     # Initializes the tools package
│       ├── weather.py      # OpenWeatherMap API integration
│       ├── math_tool.py    # Safe math expression evaluator
│       └── llm_tool.py     # Google Gemini LLM integration
├── Dockerfile              # Docker configuration for containerization
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (API keys) - IMPORTANT: Do not commit to Git!
└── README.md               # Project documentation
```
