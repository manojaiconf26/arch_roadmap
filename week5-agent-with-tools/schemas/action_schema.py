# Allowed agent outputs
from typing import TypedDict, Dict, Any, Literal


class Action(TypedDict):
    action: Literal["calculate", "lookup", "final"]
    arguments: Dict[str, Any]
