from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
import json
import csv
from io import StringIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Groq model
groq_model = LiteLLMModel(
    model_id="groq/llama-3.1-8b-instant",
    params={
        "api_key": os.getenv("GROQ_API_KEY"),
        "max_tokens": 4000,
        "temperature": 0.7
    }
)

@tool
def parse_json_tool(data: str) -> str:
    """Parse JSON string and return formatted result"""
    try:
        parsed = json.loads(data)
        return f"Successfully parsed JSON: {json.dumps(parsed, indent=2)}"
    except Exception as e:
        return f"Error parsing JSON: {str(e)}"

@tool
def to_json_tool(data: str) -> str:
    """Convert data to JSON format"""
    try:
        # Try to structure the data
        structured = {
            "timestamp": "2024-01-01T00:00:00Z",
            "source": "data_processor",
            "content": data
        }
        return json.dumps(structured, indent=2)
    except Exception as e:
        return f"Error converting to JSON: {str(e)}"

@tool
def parse_csv_tool(data: str) -> str:
    """Parse CSV string and return formatted result"""
    try:
        reader = csv.DictReader(StringIO(data))
        rows = list(reader)
        return f"Successfully parsed CSV with {len(rows)} rows: {json.dumps(rows, indent=2)}"
    except Exception as e:
        return f"Error parsing CSV: {str(e)}"

@tool
def structure_data_tool(raw_data: str, format_type: str = "json") -> str:
    """Structure raw data into specified format"""
    try:
        structured = {
            "timestamp": "2024-01-01T00:00:00Z",
            "source": "web_research",
            "data": raw_data,
            "format": format_type
        }
        
        if format_type == "json":
            return json.dumps(structured, indent=2)
        elif format_type == "csv":
            # Convert to CSV format
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=structured.keys())
            writer.writeheader()
            writer.writerow(structured)
            return output.getvalue()
        else:
            return str(structured)
    except Exception as e:
        return f"Error structuring data: {str(e)}"

# Create Data Processor Agent
data_processor_agent = Agent(
    model=groq_model,
    system_prompt="""You are a data processing specialist. Your job is to:
1. Parse and structure raw data
2. Convert between different data formats (JSON, CSV)
3. Clean and organize information
4. Handle batch data processing tasks
Provide structured output directly without using tools.""",
    tools=[]
)

def process_data(task: dict) -> dict:
    """Execute data processing task using the agent"""
    operation = task.get("operation", "")
    
    if operation == "structure_findings":
        findings = task.get("findings", [])
        format_type = task.get("format", "json")
        prompt = f"Structure the following research findings into {format_type} format:\n\n{findings}"
    elif operation == "parse_data":
        data = task.get("data", "")
        input_format = task.get("input_format", "json")
        output_format = task.get("output_format", "json")
        prompt = f"Parse this {input_format} data and convert to {output_format}:\n\n{data}"
    else:
        prompt = f"Handle data processing operation: {operation} with parameters: {task}"
    
    result = data_processor_agent(prompt)
    
    return {
        "status": "completed",
        "operation": operation,
        "result": result.message,
        "agent": "data_processor_agent"
    }