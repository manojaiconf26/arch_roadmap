# Allowed agent outputs
from typing import TypedDict, Dict, Literal, Any


class Action(TypedDict):
    action: Literal["calculate", "lookup", "final"]
    arguments: Dict[str, Any]
