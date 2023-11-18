import bcrypt
import databases

from typing import Any

import settings

class User:
    def __init__(
        self,
        id: int,
        name: str,
        email: str,
        privileges: int,
    ) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.privileges = privileges
        
    def __repr__(self) -> str:
        return f"<{self.name} ({self.id})>"
    
    @property
    def url(self) -> str:
        return f"https://undeniab.ly/{self.name}"
    
    @staticmethod
    def from_dict(user: dict[str, Any]):
        return User(**user)
    
    @staticmethod
    def name_safe(name: str) -> str:
        return name.lower().replace(" ", "-")
    
    @staticmethod
    async def signup(name: str, email: str, pw_bcrypt: bytes):
        async with databases.Database(settings.DB_DSN) as db:
            await db.execute("INSERT INTO users (name, name_safe, email, pw_bcrypt) VALUES (:name, :name_safe, :email, :pw_bcrypt)", {
                "name": name,
                "name_safe": User.name_safe(name),
                "email": email,
                "pw_bcrypt": pw_bcrypt
            })
            
            return User(**await db.fetch_one("SELECT id, name, email, privileges FROM users WHERE name = :name", {"name": name}))
    
    @staticmethod
    async def login(name: str, password: str):
        async with databases.Database(settings.DB_DSN) as db:
            user = await db.fetch_one("SELECT id, name, email, privileges, pw_bcrypt FROM users WHERE name_safe = :name_safe", {"name_safe": User.name_safe(name)})
            
            if user and bcrypt.checkpw(password.encode(), user["pw_bcrypt"].encode()):
                return User(user.id, user.name, user.email, user.privileges)
            
            return None