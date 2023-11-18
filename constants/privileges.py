from enum import IntFlag, unique
from typing import Any, Optional

def escape_enum(
    val: Any, 
    _: Optional[dict[object, object]] = None,
    ) -> str:
    return str(int(val))

@unique
@escape_enum
class Privileges(IntFlag):
    UNBANNED = 1 << 0
    VERIFIED = 1 << 1
    
    PREMIUM = 1 << 2
    
    STAFF = 1 << 3
