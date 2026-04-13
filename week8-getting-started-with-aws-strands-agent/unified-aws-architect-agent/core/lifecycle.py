#!/usr/bin/env python3
"""Agent Lifecycle - Minimal tracking"""
from enum import Enum
from datetime import datetime

class LifecycleStage(Enum):
    INPUT_HANDLING = "input_handling"
    PLANNING = "planning"
    TOOL_SELECTION = "tool_selection"
    TOOL_EXECUTION = "tool_execution"
    EVALUATION = "evaluation"
    RESPONSE_FINALIZATION = "response_finalization"
    SESSION_UPDATE = "session_update"

class LifecycleTracker:
    def __init__(self):
        self.events = []
        self.current_stage = None
        self.stage_start = None
    
    def start_stage(self, stage: LifecycleStage, metadata=None):
        self.current_stage = stage
        self.stage_start = datetime.now()
        print(f"\n{'='*60}")
        print(f"LIFECYCLE: {stage.value.upper()} - STARTED")
        print(f"{'='*60}")
    
    def end_stage(self, metadata=None):
        if self.current_stage and self.stage_start:
            duration = (datetime.now() - self.stage_start).total_seconds() * 1000
            self.events.append({"stage": self.current_stage.value, "duration_ms": duration})
            print(f"LIFECYCLE: {self.current_stage.value.upper()} - COMPLETED ({duration:.2f}ms)")
            print(f"{'='*60}\n")
            self.current_stage = None
    
    def get_summary(self):
        return {
            "total_stages": len(self.events),
            "total_duration_ms": sum(e["duration_ms"] for e in self.events),
            "stages": self.events
        }
