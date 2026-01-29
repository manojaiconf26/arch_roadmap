from agents.doer import DoerAgent
from agents.evaluator import EvaluatorAgent


class AgentController:
    def __init__(self, max_retries: int = 2):
        self.doer = DoerAgent()
        self.evaluator = EvaluatorAgent()
        self.max_retries = max_retries

    def run(self, task: str):
        feedback = None

        for attempt in range(1, self.max_retries + 2):
            print(f"\n🧠 Attempt {attempt}")

            answer = self.doer.generate(task, feedback)
            print("\nDoer Output:")
            print(answer)

            evaluation = self.evaluator.evaluate(task, answer)
            print("\nEvaluator Result:")
            print(
                f"Score: {evaluation.score}, "
                f"Pass: {evaluation.pass_result}, "
                f"Feedback: {evaluation.feedback}"
            )

            if evaluation.pass_result:
                print("\n✅ Final Answer Accepted")
                return answer

            feedback = evaluation.feedback
            print("\n🔁 Retrying with feedback...")

        print("\n❌ Failed to produce acceptable answer")
        return None
