"""
memory/ingestion.py

Ingests raw user input into memory.
No intelligence here — just storage.
"""

def ingest_memory(memory_store, user_input: str):
    memory_store.add_entry(user_input)
