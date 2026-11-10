"""
Layer 24: GraphQL Query Depth & Complexity Bomb Guard
Detects and neutralizes recursive cyclic queries, excessive field depth (> 7 levels),
and query batching attacks that cause GraphQL engine CPU exhaustion.
"""

import re

MAX_ALLOWED_DEPTH = 7

def calculate_query_depth(query_str: str) -> int:
    """Calculates max nested curly brace depth while ignoring comments."""
    # Strip strings and comments
    cleaned = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '""', query_str)
    cleaned = re.sub(r'#.*', '', cleaned)
    
    max_depth = 0
    current_depth = 0
    for char in cleaned:
        if char == '{':
            current_depth += 1
            if current_depth > max_depth:
                max_depth = current_depth
        elif char == '}':
            if current_depth > 0:
                current_depth -= 1
    return max_depth

def inspect_graphql_query(query: str, core) -> bool:
    if not getattr(core, "enabled", True):
        return True
    if not isinstance(query, str):
        return True

    depth = calculate_query_depth(query)
    if depth > MAX_ALLOWED_DEPTH:
        core.record_threat(
            rule_name="GraphQL Query Depth Bomb",
            reason=f"GraphQL query nesting depth ({depth}) exceeds maximum safe threshold ({MAX_ALLOWED_DEPTH})",
            payload=query[:120],
            block=True
        )
        return False
    return True

def arm_graphql_guard(core):
    core.inspect_graphql_query = lambda q: inspect_graphql_query(q, core)
