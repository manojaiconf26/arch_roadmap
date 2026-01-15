from orchestrator.orchestrator import Orchestrator

if __name__ == "__main__":
    orchestrator = Orchestrator()

    orchestrator.handle_user_input("I prefer AWS services")
    orchestrator.handle_user_input("Suggest a data analytics platform")

    orchestrator.handle_user_input("Compare data warehouses")

    orchestrator.handle_user_input("I want short answers")
    orchestrator.handle_user_input("Suggest a data analytics platform")
