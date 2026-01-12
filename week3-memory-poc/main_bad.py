from memory import SharedMemory, LongTermMemory
from agent import Planner, Executor, Critic
from orchestrator import Orchestrator


def main():
    print("=== Memory PoC Demo ===")

    shared_memory = SharedMemory()
    long_term_memory = LongTermMemory()

    planner = Planner("Planner", shared_memory, long_term_memory)
    executor = Executor("Executor", shared_memory)
    critic = Critic("Critic", shared_memory)

    orchestrator = Orchestrator(
        planner,
        executor,
        critic,
        long_term_memory
    )

    task_name = "build_web_app"

    evaluation = orchestrator.run_bad(task_name)

    print("\nFinal evaluation score:", evaluation["score"])
    print("\nMemory Demo:")
    print("Planner private memory:", planner.private_memory)
    print("Shared memory snapshot:", shared_memory.dump())


if __name__ == "__main__":
    main()
