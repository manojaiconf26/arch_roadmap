# Task-scoped orchestration state
"""
state.py

Represents short-lived, task-scoped state.
This is NOT memory and must never persist across tasks.
"""

class State:
    def __init__(self):
        self.step = 0
        self.last_decision = None
