"""
agent.py

The agent is a pure decision-making unit.
It does NOT:
- Loop
- Persist memory
- Control execution flow
"""

from agent.state import State
from memory.retrieval import retrieve_relevant_memory

class Agent:
    def __init__(self, memory_store):
        self.memory_store = memory_store

    def handle_task(self, task):
        """
        One agent invocation:
        observe → decide → act
        """
        state = State()
        state.step += 1

        # OBSERVE: intentionally retrieve interpreted memory
        memory = retrieve_relevant_memory(self.memory_store)

        # DECIDE
        decision = self.decide(task, memory)

        # ACT
        state.last_decision = decision
        return decision

    def decide(self, task, memory):
        """
        Same task + different memory = different outcome.
        """
        preferred_cloud = memory.get("preferred_cloud")
        response_style = memory.get("response_style")

        # if preferred_cloud == "AWS":
        #     response = (
        #         f"For '{task}', I recommend AWS-native services like "
        #         "Amazon Redshift for warehousing, Athena for ad-hoc querying, "
        #         "and AWS Glue for ETL and data integration workloads."
        #     )
        # else:
        #     response = (
        #         f"For '{task}', consider cloud-agnostic platforms "
        #         "like Snowflake or BigQuery."
        #     )
        #
        # if response_style == "concise":
        #     response = response.split(".")[0] + "."
        if preferred_cloud == "AWS":
            if response_style == "concise":
                response = (
                    f"For '{task}', use AWS services like Amazon Redshift and Athena."
                )
            else:
                response = (
                    f"For '{task}', I recommend AWS-native services like "
                    "Amazon Redshift for warehousing, Athena for ad-hoc querying, "
                    "and AWS Glue for ETL and data integration workloads."
                )
        else:
            response = (
                f"For '{task}', consider cloud-agnostic platforms "
                "like Snowflake or BigQuery."
            )


        return response
