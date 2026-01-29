from models.evaluation_result import EvaluationResult


class EvaluatorAgent:
    def evaluate(self, task: str, answer: str) -> EvaluationResult:
        """
        Evaluates the doer's output based on simple quality criteria.
        """

        score = 0
        feedback = []

        # Beginner-friendly length check
        if len(answer.split()) >= 40:
            score += 2
        else:
            feedback.append("The explanation is too short for a beginner.")

        # Concept correctness check
        if "goal" in answer and "actions" in answer:
            score += 2
        else:
            feedback.append("Missing goal-oriented or action-based explanation.")

        # Paragraph structure check
        if answer.count(".") <= 3:
            score += 1
        else:
            feedback.append("The explanation should be a single clear paragraph.")

        return EvaluationResult(
            score=score,
            pass_result=score >= 4,
            feedback=" ".join(feedback) if feedback else "Good explanation."
        )
