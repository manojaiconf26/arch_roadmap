# Evaluates outcomes (signal only)
class Critic:
    def evaluate(self, execution_result: str):
        if "Research" in execution_result:
            return "bad"
        return "good"
