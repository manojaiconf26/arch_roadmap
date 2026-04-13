#!/usr/bin/env python3
"""Runtime Steering - Minimal behavioral control"""
from enum import Enum

class VerbosityLevel(Enum):
    CONCISE = "concise"
    DETAILED = "detailed"
    EXPERT = "expert"

class RiskTolerance(Enum):
    COST_OPTIMIZED = "cost_optimized"
    BALANCED = "balanced"
    PERFORMANCE = "performance"

class SteeringConfig:
    def __init__(self):
        self.verbosity = VerbosityLevel.DETAILED
        self.risk_tolerance = RiskTolerance.BALANCED
    
    def to_prompt_guidance(self):
        guidance = []
        if self.verbosity == VerbosityLevel.CONCISE:
            guidance.append("Provide concise, technical responses.")
        elif self.verbosity == VerbosityLevel.DETAILED:
            guidance.append("Provide detailed, step-by-step explanations.")
        else:
            guidance.append("Provide advanced technical depth.")
        
        if self.risk_tolerance == RiskTolerance.COST_OPTIMIZED:
            guidance.append("Prioritize cost-effective solutions.")
        elif self.risk_tolerance == RiskTolerance.PERFORMANCE:
            guidance.append("Prioritize performance over cost.")
        
        return "\n".join(guidance)
    
    def to_dict(self):
        return {
            "verbosity": self.verbosity.value,
            "risk_tolerance": self.risk_tolerance.value
        }

class SteeringManager:
    def __init__(self):
        self.config = SteeringConfig()
    
    def update(self, **kwargs):
        if "verbosity" in kwargs:
            self.config.verbosity = VerbosityLevel(kwargs["verbosity"])
        if "risk_tolerance" in kwargs:
            self.config.risk_tolerance = RiskTolerance(kwargs["risk_tolerance"])
        print(f"\n🎯 STEERING UPDATED: {self.config.to_dict()}\n")
    
    def get_prompt_guidance(self):
        return self.config.to_prompt_guidance()
    
    def get_config(self):
        return self.config
