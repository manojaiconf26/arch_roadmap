from controller.agent_controller import AgentController


def main():
    task = "Explain what an agent is in one paragraph for a beginner."

    controller = AgentController(max_retries=2)
    controller.run(task)


if __name__ == "__main__":
    main()
