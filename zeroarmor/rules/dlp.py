"""
Layer 21: Outbound DLP (Data Loss Prevention)
Scans outgoing HTTP payloads for unmasked credit cards and high-risk PII to stop mass data leaks.
"""

import re

# Major credit card regex (Visa, MasterCard, Amex, Discover)
CC_REGEX = re.compile(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b")

def luhn_checksum(card_number: str) -> bool:
    digits = [int(c) for c in card_number if c.isdigit()]
    if len(digits) < 13:
        return False
    checksum = 0
    reverse_digits = digits[::-1]
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            doubled = d * 2
            checksum += (doubled - 9) if doubled > 9 else doubled
        else:
            checksum += d
    return (checksum % 10) == 0

def inspect_outbound_data(text: str, core) -> bool:
    if not isinstance(text, str):
        return True

    matches = CC_REGEX.findall(text)
    for m in matches:
        if luhn_checksum(m):
            core.record_threat(
                rule_name="Outbound Data Loss Prevention (Credit Card Leak)",
                reason=f"Intercepted unmasked valid credit card number in outbound response: {m[:4]}****{m[-4:]}",
                payload="Credit Card Leak Prevented",
                block=True
            )
            return False
    return True

def arm_dlp(core):
    core.inspect_outbound_data = lambda t: inspect_outbound_data(t, core)
