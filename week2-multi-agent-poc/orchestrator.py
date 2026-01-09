# orchestrator.py
"""
Planner → Executor (Bad) → Critic orchestration → Feedback → Executor
"""

from agents.planner import run_planner
from agents.executor_bad import run_executor
from agents.critic import run_critic
from config import MAX_CRITIC_RETRIES
from time import sleep


def load_prompt(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

def main():
    goal = "Create a 3-step Kubernetes learning plan for a backend developer"

    planner_prompt = load_prompt("prompts/planner.txt")
    executor_prompt = load_prompt("prompts/executor_bad.txt")
    critic_prompt = load_prompt("prompts/critic.txt")

    print("\n--- PLANNER ---")
    plan = run_planner(goal, planner_prompt)
    print(plan)
    print(f"Planner plan:\n {plan}")

    feedback = None

    for attempt in range(1, MAX_CRITIC_RETRIES + 1):
        print(f"\n--- EXECUTOR (Attempt {attempt}) ---")
        output = run_executor(plan, feedback, executor_prompt)
        print(f"Executor output:\n {output}")

        print("\n--- CRITIC ---")
        status, feedback = run_critic(output, critic_prompt)
        print(f"Critic status ---> {status}")

        sleep (15)
        print("\n--- <<<<<<< sleep for 15 seconds >>>>>> ---")

        if status == "APPROVED":
            print("\n✅ FINAL OUTPUT::::::")
            print(output)
            return

        print("\n🔁 REVISION REQUIRED")

    print("\n❌ Failed after max retries")

if __name__ == "__main__":
    main()
