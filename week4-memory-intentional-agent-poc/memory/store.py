"""
memory/store.py

Simple in-memory store for raw conversation history.
Week 3 responsibility: storage only.
"""

class MemoryStore:
    def __init__(self):
        self._entries = []

    def add_entry(self, entry: str):
        self._entries.append(entry)

    def get_all(self):
        return self._entries
