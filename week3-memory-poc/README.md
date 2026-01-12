# Week 3 Memory PoC

Multi-agent system with memory management demonstrating private, shared, and long-term memory.

## Structure

```
week3-memory-poc/
├── agent.py            # Planner, Executor, Critic classes with private memory
├── memory.py           # Shared memory + long-term memory management
├── orchestrator.py     # Orchestrates agent workflow
├── main.py             # Entry point
└── long_term_memory.json  # Persistent storage
```

## Memory Types

- **Private Memory**: Each agent has isolated memory (`dict`)
- **Shared Memory**: Inter-agent communication (`dict`)
- **Long-term Memory**: Persistent storage (JSON file)

## Execution

**Success scenario:**
```bash
cd week3-memory-poc
python main.py
```

**Failure scenario:**
```bash
cd week3-memory-poc
python main_bad.py
```

## Workflow

1. Planner creates plan → stores in private memory
2. Executor runs plan → stores result in private memory
3. Critic evaluates → stores evaluation in private memory
4. All data shared via SharedMemory and persisted to LongTermMemory