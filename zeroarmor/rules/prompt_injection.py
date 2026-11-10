"""
Layer 23: Prompt Injection & LLM Jailbreak RASP (AI Security Shield)
Protects AI applications, agents, and LLM backends against prompt injection,
system prompt extraction, jailbreak persona overrides (DAN, Developer Mode),
and prompt smuggling delimiters.
"""

import re

PROMPT_INJECTION_PATTERNS = [
    # 1. System Prompt Overrides & Instruction Wiping
    re.compile(r"\b(ignore|disregard|forget|override)\s+(all\s+)?(previous|prior|above|system)\s+(instructions|prompts|rules|commands|context)\b", re.IGNORECASE),
    re.compile(r"\b(system\s+prompt\s+override|new\s+system\s+instruction)\b", re.IGNORECASE),
    
    # 2. System Prompt & Secret Extraction
    re.compile(r"\b(show|reveal|repeat|output|print|dump)\s+(me\s+)?(your|the)?\s*(system\s+prompt|initial\s+instructions|system\s+message|hidden\s+rules)\b", re.IGNORECASE),
    re.compile(r"\b(what\s+are\s+your\s+exact\s+system\s+instructions)\b", re.IGNORECASE),
    
    # 3. Known Jailbreak Personas & Filter Bypasses
    re.compile(r"\b(you\s+are\s+now\s+(DAN|unfiltered|jailbroken|evil\s+bot|chaos\s+gpt))\b", re.IGNORECASE),
    re.compile(r"\b(developer\s+mode\s+enabled|jailbreak\s+activated|act\s+as\s+an\s+unrestricted\s+ai)\b", re.IGNORECASE),
    re.compile(r"\b(do\s+anything\s+now|bypass\s+all\s+(filters|guidelines|guardrails))\b", re.IGNORECASE),
    
    # 4. Delimiter Hijacking & Special Token Injections
    re.compile(r"(\[START_RAW_PROMPT\]|<\|im_start\|>system|<\|im_end\|>|\[SYSTEM_INSTRUCTION\])", re.IGNORECASE),
    
    # 5. Base64 Smuggling Instructions
    re.compile(r"\b(decode\s+the\s+following\s+base64\s+and\s+(execute|follow|run))\b", re.IGNORECASE)
]

def inspect_prompt(text: str, core) -> bool:
    if not getattr(core, "enabled", True):
        return True
    if not isinstance(text, str):
        return True

    clean_text = text.strip()
    for pattern in PROMPT_INJECTION_PATTERNS:
        match = pattern.search(clean_text)
        if match:
            core.record_threat(
                rule_name="LLM Prompt Injection & Jailbreak",
                reason=f"Detected adversarial prompt injection payload: '{match.group(0)}'",
                payload=clean_text[:120],
                block=True
            )
            return False
    return True

def arm_prompt_injection(core):
    core.inspect_prompt = lambda t: inspect_prompt(t, core)
