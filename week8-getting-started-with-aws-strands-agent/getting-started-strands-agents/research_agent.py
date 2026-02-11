from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Groq model
groq_model = LiteLLMModel(
    model_id="groq/llama-3.3-70b-versatile",
    params={
        "api_key": os.getenv("GROQ_API_KEY"),
        "max_tokens": 4000,
        "temperature": 0.7
    }
)

@tool
def web_search_tool(query: str) -> str:
    """Search the web for information"""
    # Simulated web search - in real implementation use actual search API
    return f"Search results for '{query}': Found relevant information about {query} from multiple sources."

@tool
def get_content_tool(url: str) -> str:
    """Get content from a URL"""
    return f"Content retrieved from {url}: Detailed information about the topic."

# Create Research Agent
research_agent = Agent(
    model=groq_model,
    system_prompt="""You are a research specialist. Your job is to:
1. Search for information on given topics
2. Gather detailed content from multiple sources
3. Provide comprehensive research summaries
Use the available tools to search and retrieve information.""",
    tools=[web_search_tool, get_content_tool]
)

def research_topic(topic: str) -> dict:
    """Execute research task using the agent"""
    prompt = f"Research the topic: {topic}. Provide a comprehensive summary with key findings."
    result = research_agent(prompt)
    
    return {
        "status": "completed",
        "topic": topic,
        "findings": result.message,
        "agent": "research_agent"
    }