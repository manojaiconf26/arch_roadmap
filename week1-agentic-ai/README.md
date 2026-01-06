# Week 1: From Prompts to Agentic Systems

This project demonstrates the difference between a simple **chatbot** and a **goal-driven agent loop** using **Groq**. It aligns with the Week 1 blog in the *Agentic AI Architecture* series.

---

## Project Structure

```
week1-agentic-ai/
├── README.md          # Project overview and instructions
├── requirements.txt   # Python dependencies
├── chatbot.py         # Single prompt-response chatbot
└── agent_loop.py      # Goal-driven agent loop
```

---

## Setup Instructions

1. **Clone the repository** (or download the zip):

```bash
git clone https://github.com/yourusername/week1-agentic-ai.git
cd week1-agentic-ai
```

2. **Create a virtual environment** (recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Set your Groq API key**:

```bash
export GROQ_API_KEY=your_key_here  # Linux/macOS
set GROQ_API_KEY=your_key_here     # Windows
```

---

## Running the PoC

### 1️⃣ Chatbot (Prompt-Only)

```bash
python chatbot.py
```

**Expected Output:**

- A **single response** generated for the 3-step Kubernetes learning plan.
- No iteration or state maintenance.

---

### 2️⃣ Goal-Driven Agent Loop

```bash
python agent_loop.py
```

**Expected Output:**

- Iteratively builds a 3-step Kubernetes learning plan.
- Maintains **internal state** and stops autonomously when the goal is complete.

---

## Key Insights

- **Chatbot**: reactive, single-shot response.  
- **Agent loop**: iterative, goal-driven, maintains state.  
- Demonstrates that **control flow creates agency**, not the model itself.

---

## Optional Enhancements

- Add logging for each step in `agent_loop.py`.
- Experiment with different models in `Groq` (e.g., `llama-3.1-8b-instant`).
- Extend to handle multiple goals or longer workflows.

---

## GitHub Repository Placeholder

[https://github.com/yourusername/week1-agentic-ai](#)
