import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = """
Create a 3-step learning plan for Kubernetes
for a backend developer.
"""

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}]
)

print("Chatbot Output:")
print(response.choices[0].message.content)