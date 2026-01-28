# Shared agent state
class AgentState:
    def __init__(self, goal: str):
        self.goal = goal
        self.plan = []
        self.current_step_index = 0
        self.history = []
        self.completed = False

    def current_step(self):
        if self.current_step_index < len(self.plan):
            return self.plan[self.current_step_index]
        return None
