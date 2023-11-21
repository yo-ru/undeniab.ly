from enum import IntFlag, unique

@unique
class Privileges(IntFlag):
    UNBANNED = 1 << 0
    VERIFIED = 1 << 1
    
    PREMIUM = 1 << 2
    
    STAFF = 1 << 3
