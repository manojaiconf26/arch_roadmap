from dataclasses import dataclass


@dataclass
class EvaluationResult:
    score: int
    pass_result: bool
    feedback: str
