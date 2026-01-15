# Architectural explanation
# Week 4 — Intentional Memory-Driven Agent

This PoC demonstrates:

- State used for orchestration (Week 3)
- Memory used for decision shaping (Week 4)
- Observe → Decide → Act inside the agent
- Loop controlled by orchestration layer

The agent does not self-loop.
Memory persists across calls and influences behavior.

✅ What This PoC Proves (Architecturally)

✔ Agent ≠ chatbot
✔ Agent ≠ loop
✔ Memory ≠ state
✔ Decisions evolve over time
✔ Orchestration controls execution