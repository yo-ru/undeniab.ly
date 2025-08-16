from __future__ import annotations

from enum import IntFlag
from enum import unique

@unique
class Badges(IntFlag):
    VERIFIED = 1 << 0

    PREMIUM = 1 << 1

    STAFF = 1 << 2

    RICH = 1 << 3

    @staticmethod
    def has_badge(badges: int, badge: Badges) -> bool:
        return badges & badge