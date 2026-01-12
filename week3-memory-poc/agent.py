class Agent:
    def __init__(self, name, shared_memory):
        self.name = name
        self.shared_memory = shared_memory
        self.private_memory = {}

    def remember(self, key, value):
        self.private_memory[key] = value
        print(f"{self.name} remembered: {key}")


class Planner(Agent):
    def __init__(self, name, shared_memory, long_term_memory):
        super().__init__(name, shared_memory)
        self.long_term_memory = long_term_memory

    def plan(self, task):
        print(f"Planner creating plan for: {task}")

        past_run = self.long_term_memory.read(f"workflow_{task}")

        if past_run and past_run["score"] < 7:
            steps = ["re-analyze", "refine design", "re-implement carefully"]
        else:
            steps = ["analyze", "design", "implement"]

        plan = {"task": task, "steps": steps}

        self.remember("task", task)
        self.remember("steps", steps)

        self.shared_memory.write("current_plan", plan)
        return plan


class Executor(Agent):
    def execute(self, plan):
        print(f"Executor executing plan for: {plan['task']}")
        result = f"Executed plan for: {plan['task']}"
        self.remember("last_execution", result)
        self.shared_memory.write("execution_result", result)
        return result


class Critic(Agent):
    def evaluate(self, result):
        print(f"Critic evaluating result: {result}")

        score = 8 if "Executed" in result else 4
        evaluation = {"score": score}

        self.remember("last_evaluation", evaluation)
        self.shared_memory.write("evaluation", evaluation)
        return evaluation

    def evaluate_bad(self, result):
        print(f"Critic evaluating result: {result}")

        score = 6 if "Executed" in result else 4
        evaluation = {"score": score}

        self.remember("last_evaluation", evaluation)
        self.shared_memory.write("evaluation", evaluation)
        return evaluation
