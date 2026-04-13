#!/usr/bin/env python3
"""AWS Solutions Architect Agent - Simplified"""
import os
from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel, GroqModel

import sys
sys.path.append(os.path.dirname(__file__))

from core.lifecycle import LifecycleTracker, LifecycleStage
from steering.steering_config import SteeringManager
from hooks.agent_hooks import PreToolValidationHook, PostToolNormalizationHook, PreResponseFormattingHook, EvaluationGateHook
from sessions.session_state import SessionManager

load_dotenv()

class AWSArchitectAgent:
    """AWS Solutions Architect Agent with 4-layer control"""
    
    def __init__(self, session_id, user_id, provider=None):
        self.lifecycle = LifecycleTracker()
        self.steering = SteeringManager()
        self.session = SessionManager(session_id, user_id)
        self.hooks = [
            PreToolValidationHook(),
            PostToolNormalizationHook(),
            PreResponseFormattingHook(),
            EvaluationGateHook()
        ]
        
        provider = provider or os.getenv("PROVIDER", "groq")
        
        if provider == "groq":
            self.model = GroqModel(
                model_id="llama-3.1-8b-instant",
                api_key=os.getenv("GROQ_API_KEY"),
                temperature=0.7,
                max_tokens=2000
            )
        else:
            model_id = os.getenv("MODEL_ID", "anthropic.claude-sonnet-4-5-20250929-v1:0")
            self.model = BedrockModel(model_id=model_id, temperature=0.7, max_tokens=2000)
        
        self.agent = Agent(
            model=self.model,
            system_prompt=self._build_prompt(),
            hooks=self.hooks
        )
    
    def _build_prompt(self):
        base = "You are an expert AWS Solutions Architect.\n\n"
        return base + self.steering.get_prompt_guidance() + "\n" + self.session.get_context_for_agent()
    
    def update_steering(self, **kwargs):
        self.steering.update(**kwargs)
        self.agent.system_prompt = self._build_prompt()
    
    def process(self, query):
        print("\n" + "="*80)
        print("AWS ARCHITECT AGENT - PROCESSING")
        print("="*80)
        
        # Lifecycle stages
        self.lifecycle.start_stage(LifecycleStage.INPUT_HANDLING)
        self.lifecycle.end_stage()
        
        self.lifecycle.start_stage(LifecycleStage.PLANNING)
        self.lifecycle.end_stage()
        
        self.lifecycle.start_stage(LifecycleStage.TOOL_EXECUTION)
        result = self.agent(query)
        self.lifecycle.end_stage()
        
        self.lifecycle.start_stage(LifecycleStage.EVALUATION)
        self.lifecycle.end_stage()
        
        self.lifecycle.start_stage(LifecycleStage.RESPONSE_FINALIZATION)
        response = str(result.message)
        self.lifecycle.end_stage()
        
        self.lifecycle.start_stage(LifecycleStage.SESSION_UPDATE)
        self.session.get_state().increment_turn()
        self.session.get_state().add_to_history({"query": query[:50]})
        self.lifecycle.end_stage()
        
        return {
            "response": response,
            "lifecycle": self.lifecycle.get_summary(),
            "session": self.session.get_state().to_dict()
        }
    
    def print_hierarchy(self):
        print("\n" + "="*80)
        print("CONTROL HIERARCHY")
        print("="*80)
        print("Layer 1: System Prompt - AWS Solutions Architect")
        print(f"Layer 2: Steering - {self.steering.get_config().to_dict()}")
        print(f"Layer 3: Hooks - {len(self.hooks)} active")
        print(f"Layer 4: Evaluation - Cost/Quality gates")
        print("="*80 + "\n")

def main():
    print("\n" + "#"*80)
    print("SCENARIO 1: GROQ LLAMA 3.1 8B")
    print("#"*80)
    
    agent = AWSArchitectAgent("demo_001", "alice", provider="groq")
    agent.session.update_profile(expertise_level="beginner", cost_sensitivity="high")
    agent.update_steering(verbosity="detailed", risk_tolerance="cost_optimized")
    agent.print_hierarchy()
    
    result = agent.process("I need to build a REST API for my mobile app. What AWS services should I use?")
    print("\n📝 RESPONSE:")
    print(result["response"])
    print(f"\n📊 LIFECYCLE: {result['lifecycle']['total_duration_ms']:.2f}ms, {result['lifecycle']['total_stages']} stages")
    
    print("\n\n" + "#"*80)
    print("SCENARIO 2: BEDROCK CLAUDE SONNET 4.5")
    print("#"*80)
    
    agent2 = AWSArchitectAgent("demo_002", "bob", provider="bedrock")
    agent2.session.update_profile(expertise_level="expert", cost_sensitivity="low")
    agent2.update_steering(verbosity="concise", risk_tolerance="performance")
    agent2.print_hierarchy()
    
    result2 = agent2.process("Design a serverless data processing pipeline with DynamoDB Streams")
    print("\n📝 RESPONSE:")
    print(result2["response"])

if __name__ == "__main__":
    main()
