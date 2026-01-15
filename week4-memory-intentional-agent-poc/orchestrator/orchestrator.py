from agent.agent import Agent
from memory.store import MemoryStore
from memory.ingestion import ingest_memory

class Orchestrator:
    def __init__(self):
        self.memory_store = MemoryStore()
        self.agent = Agent(self.memory_store)

    def handle_user_input(self, user_input: str):
        print(f"\nUser: {user_input}")

        # Store memory
        ingest_memory(self.memory_store, user_input)

        # Decide whether to invoke agent
        if self.is_task(user_input):
            response = self.agent.handle_task(user_input)
            print(f"Agent: {response}")

    def is_task(self, user_input: str) -> bool:
        """
        Simple heuristic:
        Preference statements → memory only
        Questions / commands → agent invocation
        """
        lowered = user_input.lower()
        return any(
            keyword in lowered
            for keyword in ["suggest", "compare", "recommend"]
        )
