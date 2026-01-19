from agent.agent import Agent


def main():
    agent = Agent()

    while True:
        user_input = input("\nUser > ")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = agent.run(user_input)
        print(f"Agent > {response}")


if __name__ == "__main__":
    main()
