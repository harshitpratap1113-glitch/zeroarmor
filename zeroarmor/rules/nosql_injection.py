"""
Layer 26: NoSQL & MongoDB Operator Injection Jail
Detects and neutralizes query selector tampering ($where, $ne, $gt, $regex, $nin)
in untrusted input payloads that attempt to bypass authentication in document databases.
"""

import re
from typing import Any

NOSQL_OPERATOR_PATTERN = re.compile(
    r'("\$(where|ne|gt|gte|lt|lte|regex|nin|or|and|nor|expr|jsonSchema)")',
    re.IGNORECASE
)

def inspect_nosql_input(data: Any, core) -> bool:
    if not getattr(core, "enabled", True):
        return True
    
    if isinstance(data, str):
        match = NOSQL_OPERATOR_PATTERN.search(data)
        if match:
            core.record_threat(
                rule_name="NoSQL Query Operator Injection",
                reason=f"Detected hazardous MongoDB/NoSQL query operator: '{match.group(0)}'",
                payload=data[:100],
                block=True
            )
            return False
            
    elif isinstance(data, dict):
        for k, v in data.items():
            if isinstance(k, str) and k.startswith("$") and k.lower() in ["$where", "$ne", "$gt", "$regex", "$nin", "$expr"]:
                core.record_threat(
                    rule_name="NoSQL Query Operator Injection",
                    reason=f"Detected hazardous MongoDB query operator key: '{k}'",
                    payload=f"Key: {k}, Value: {v}",
                    block=True
                )
                return False
            if isinstance(v, (dict, list)):
                if not inspect_nosql_input(v, core):
                    return False
                    
    elif isinstance(data, (list, tuple)):
        for item in data:
            if not inspect_nosql_input(item, core):
                return False

    return True

def arm_nosql_injection(core):
    core.inspect_nosql_input = lambda d: inspect_nosql_input(d, core)
