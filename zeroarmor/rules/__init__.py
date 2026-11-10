"""
ZeroArmor 32-Layer Titanium Rules Module Registry
"""

from .sqli import arm_sqli
from .rce import arm_rce
from .path_traversal import arm_path_traversal
from .ssrf import arm_ssrf
from .deserialization import arm_deserialization
from .eval_exec import arm_eval_exec
from .secret_scrubber import arm_secret_scrubber
from .redos import arm_redos
from .dos_limiter import arm_dos_limiter
from .attr_pollution import arm_attr_pollution
from .zip_slip import arm_zip_slip
from .temp_file import arm_temp_file
from .ssti import arm_ssti
from .headers import arm_headers
from .cors import arm_cors
from .env_guard import arm_env_guard
from .dlp import arm_dlp
from .rate_limiter import arm_rate_limiter

# Next-Gen Vectors 23-32
from .prompt_injection import arm_prompt_injection
from .graphql_guard import arm_graphql_guard
from .xxe import arm_xxe
from .nosql_injection import arm_nosql_injection
from .open_redirect import arm_open_redirect
from .jwt_guard import arm_jwt_guard
from .insecure_crypto import arm_insecure_crypto
from .yaml_gadget import arm_yaml_gadget
from .dns_rebinding import arm_dns_rebinding
from .honeytoken import arm_honeytoken

__all__ = [
    "arm_sqli",
    "arm_rce",
    "arm_path_traversal",
    "arm_ssrf",
    "arm_deserialization",
    "arm_eval_exec",
    "arm_secret_scrubber",
    "arm_redos",
    "arm_dos_limiter",
    "arm_attr_pollution",
    "arm_zip_slip",
    "arm_temp_file",
    "arm_ssti",
    "arm_headers",
    "arm_cors",
    "arm_env_guard",
    "arm_dlp",
    "arm_rate_limiter",
    "arm_prompt_injection",
    "arm_graphql_guard",
    "arm_xxe",
    "arm_nosql_injection",
    "arm_open_redirect",
    "arm_jwt_guard",
    "arm_insecure_crypto",
    "arm_yaml_gadget",
    "arm_dns_rebinding",
    "arm_honeytoken"
]
