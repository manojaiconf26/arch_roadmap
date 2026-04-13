#!/usr/bin/env python3
"""Agent Hooks - Minimal control points"""
from strands.hooks import HookProvider, HookRegistry, BeforeInvocationEvent, AfterInvocationEvent

class PreToolValidationHook(HookProvider):
    def __init__(self):
        self.blocked_count = 0
    
    def register_hooks(self, registry: HookRegistry, **kwargs):
        registry.add_callback(BeforeInvocationEvent, self.validate)
    
    def validate(self, event):
        print(f"\n🔍 PRE-TOOL HOOK: Validating")
        print(f"   ✓ Validation passed\n")

class PostToolNormalizationHook(HookProvider):
    def __init__(self):
        self.processed_count = 0
    
    def register_hooks(self, registry: HookRegistry, **kwargs):
        registry.add_callback(AfterInvocationEvent, self.normalize)
    
    def normalize(self, event):
        print(f"\n📊 POST-TOOL HOOK: Normalizing")
        self.processed_count += 1
        print(f"   ✓ Normalization complete\n")

class PreResponseFormattingHook(HookProvider):
    def register_hooks(self, registry: HookRegistry, **kwargs):
        registry.add_callback(AfterInvocationEvent, self.format_response)
    
    def format_response(self, event):
        print(f"\n✨ PRE-RESPONSE HOOK: Formatting")
        print(f"   ✓ Response formatted\n")

class EvaluationGateHook(HookProvider):
    def __init__(self, cost_threshold=100.0, quality_threshold=0.7):
        self.cost_threshold = cost_threshold
        self.quality_threshold = quality_threshold
        self.evaluations = []
    
    def register_hooks(self, registry: HookRegistry, **kwargs):
        registry.add_callback(AfterInvocationEvent, self.evaluate)
    
    def evaluate(self, event):
        print(f"\n⚖️  EVALUATION HOOK: Checking gates")
        evaluation = {"cost": 50.0, "quality": 0.85, "passed": True}
        self.evaluations.append(evaluation)
        print(f"   ✓ Cost: ${evaluation['cost']:.2f} (threshold: ${self.cost_threshold})")
        print(f"   ✓ Quality: {evaluation['quality']:.2f} (threshold: {self.quality_threshold})")
        print(f"   ✅ EVALUATION PASSED\n")
        return evaluation
