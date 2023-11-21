from enum import IntFlag, unique

@unique
class Privileges(IntFlag):
    UNBANNED = 1 << 0
    VERIFIED = 1 << 1
    
    PREMIUM = 1 << 2
    
    STAFF = 1 << 3
    
    @staticmethod
    def has_priv(priv: "Privileges", user_priv: "Privileges") -> bool:
        return user_priv & priv != 0
