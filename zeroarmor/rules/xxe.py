"""
Layer 25: XML External Entity (XXE) & Billion Laughs Defense
Hooks xml.etree.ElementTree and DOM parsers to neutralize external entity references,
SYSTEM file directives, and XML exponential expansion bombs (Billion Laughs).
"""

import re
import sys
import xml.etree.ElementTree as ET

XXE_DANGEROUS_PATTERN = re.compile(
    r"(<!ENTITY\s+.*?(SYSTEM|PUBLIC)\s+[\"']|"
    r"<!DOCTYPE\s+.*?\[.*?<!ENTITY|"
    r"(&[a-zA-Z0-9_]+;\s*){5,})",
    re.IGNORECASE | re.DOTALL
)

def inspect_xml_string(xml_str, core) -> bool:
    if not getattr(core, "enabled", True):
        return True
    if isinstance(xml_str, (bytes, bytearray)):
        try:
            content = xml_str.decode("utf-8", "ignore")
        except Exception:
            return True
    elif isinstance(xml_str, str):
        content = xml_str
    else:
        return True

    match = XXE_DANGEROUS_PATTERN.search(content)
    if match:
        core.record_threat(
            rule_name="XML External Entity (XXE) & XML Bomb",
            reason="Blocked XML payload containing hazardous <!ENTITY / SYSTEM or recursive expansion directives",
            payload=content[:120],
            block=True
        )
        return False
    return True

def arm_xxe(core):
    # Hook xml.etree.ElementTree.fromstring
    orig_fromstring = ET.fromstring
    def armored_fromstring(text, *args, **kwargs):
        inspect_xml_string(text, core)
        return orig_fromstring(text, *args, **kwargs)
    ET.fromstring = armored_fromstring

    # Hook minidom if imported
    if "xml.dom.minidom" in sys.modules:
        try:
            import xml.dom.minidom as minidom
            orig_parse_str = minidom.parseString
            def armored_parse_str(string, *args, **kwargs):
                inspect_xml_string(string, core)
                return orig_parse_str(string, *args, **kwargs)
            minidom.parseString = armored_parse_str
        except Exception:
            pass
