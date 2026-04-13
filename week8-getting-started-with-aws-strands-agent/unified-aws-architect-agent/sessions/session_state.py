#!/usr/bin/env python3
"""Session Management - Minimal state tracking"""

class SessionState:
    def __init__(self, session_id, user_id):
        self.session_id = session_id
        self.user_id = user_id
        self.expertise_level = "intermediate"
        self.cost_sensitivity = "balanced"
        self.turn_count = 0
        self.history = []
    
    def increment_turn(self):
        self.turn_count += 1
    
    def add_to_history(self, item):
        self.history.append(item)
    
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "expertise_level": self.expertise_level,
            "turn_count": self.turn_count,
            "history_count": len(self.history)
        }

class SessionManager:
    def __init__(self, session_id, user_id):
        self.state = SessionState(session_id, user_id)
    
    def get_state(self):
        return self.state
    
    def update_profile(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)
        print(f"\n👤 SESSION: Profile updated - {kwargs}\n")
    
    def get_context_for_agent(self):
        return f"""User Context:
- Expertise: {self.state.expertise_level}
- Cost Sensitivity: {self.state.cost_sensitivity}
- Turn: {self.state.turn_count}
"""
