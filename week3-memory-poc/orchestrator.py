class Orchestrator:
    def __init__(self, planner, executor, critic, long_term_memory):
        self.planner = planner
        self.executor = executor
        self.critic = critic
        self.long_term_memory = long_term_memory

    def run(self, task):
        print("\nOrchestrator starting workflow for:", task)

        plan = self.planner.plan(task)
        result = self.executor.execute(plan)
        evaluation = self.critic.evaluate_bad(result)

        self.long_term_memory.write(
            f"workflow_{task}",
            {
                "plan": plan,
                "score": evaluation["score"]
            }
        )

        print("Workflow completed for:", task)
        return evaluation

    def run_bad(self, task):
        print("\nOrchestrator starting workflow for:", task)

        plan = self.planner.plan(task)
        result = self.executor.execute(plan)
        evaluation = self.critic.evaluate_bad(result)

        self.long_term_memory.write(
            f"workflow_{task}",
            {
                "plan": plan,
                "score": evaluation["score"]
            }
        )

        print("Workflow completed for:", task)
        return evaluation
