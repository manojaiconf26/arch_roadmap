# Executes exactly one step
class Executor:
    def execute(self, step: str):
        print(f"Executing step: {step}")
        return f"Result of [{step}]"
