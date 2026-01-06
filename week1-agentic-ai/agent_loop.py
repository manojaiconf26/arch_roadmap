import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

goal = "Create a clear 3-step Kubernetes learning plan"
state = {"steps": [], "completed": False}
MAX_STEPS = 5

for step_num in range(MAX_STEPS):
    prompt = f"""You are an AI agent.

Goal:
{goal}

Current plan:
{state["steps"]}

Decide the NEXT step to improve or add to the plan.
If the plan is complete and high quality, reply ONLY with:
DONE"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response.choices[0].message.content.strip()

    if output == "DONE":
        state["completed"] = True
        break

    state["steps"].append(output)

print("\nAgent Output:")
for i, step in enumerate(state["steps"], 1):
    print(f"{i}. {step}")