import bcrypt
import databases

from quart import session
from cmyui import log, Ansi
from typing import Any, Union

from constants.privileges import Privileges

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
    
    @staticmethod
    def from_dict(user: dict[str, Any]) -> "User":
        return User(**user)

    @staticmethod
    async def from_db(user: Union[int, str]) -> "User":
        # check if user is int or str
        if isinstance(user, int):
            query = "SELECT id, name, email, privileges FROM users WHERE id = :id"
            args = {"id": user}
        elif isinstance(user, str):
            query = "SELECT id, name, email, privileges FROM users WHERE name_safe = :name_safe"
            args = {"name_safe": User.name_safe(user)}
        
        async with databases.Database(settings.DB_DSN) as db:
            return User(**await db.fetch_one(query, args))
    
    @staticmethod
    def name_safe(name: str) -> str:
        return name.lower().replace(" ", "-")

    @staticmethod
    async def signup(name: str, email: str, password: str) -> None:
        async with databases.Database(settings.DB_DSN) as db:
            await db.execute("INSERT INTO users (name, name_safe, email, pw_bcrypt) VALUES (:name, :name_safe, :email, :pw_bcrypt)", {
                "name": name,
                "name_safe": User.name_safe(name),
                "email": email,
                "pw_bcrypt": bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            })
            
            user = await User.from_db(name)
            session["user"] = user.__dict__
            log(f"{user} has signed up!", Ansi.LGREEN)
    
    @staticmethod
    async def login(name: str, password: str) -> bool:
        async with databases.Database(settings.DB_DSN) as db:
            # NOTE: we avoid using User.from_db here because we don't want to store the password in the session
            user_db = await db.fetch_one("SELECT id, name, email, privileges, pw_bcrypt FROM users WHERE name_safe = :name_safe", {"name_safe": User.name_safe(name)})
            
            if user_db and bcrypt.checkpw(password.encode(), user_db["pw_bcrypt"].encode()):
                user = User(user_db.id, user_db.name, user_db.email, user_db.privileges)
                session["user"] = user.__dict__
                log(f"{user} has logged in!", Ansi.LGREEN)
                return True
            
            return False
    
    @staticmethod
    def logout() -> None:
        session.pop("user", None)
        
    @staticmethod
    def authenticated() -> bool:
        return "user" in session
    
    @staticmethod
    def has_privilege(privilege: Privileges) -> bool:
        if not User.authenticated():
            return False
        return User.from_dict(session["user"]).privileges & privilege != 0

    @staticmethod
    async def available_name(name: str) -> bool:
        async with databases.Database(settings.DB_DSN) as db:
            return not await db.fetch_one("SELECT 1 FROM users WHERE name_safe = :name_safe", {"name_safe": User.name_safe(name)})

    @staticmethod
    async def available_email(email: str) -> bool:
        async with databases.Database(settings.DB_DSN) as db:
            return not await db.fetch_one("SELECT 1 FROM users WHERE email = :email", {"email": email})

    @staticmethod
    async def change_password(user: Union[int, str], password: str) -> bool:
        if isinstance(user, int):
            query = "UPDATE users SET pw_bcrypt = :pw_bcrypt WHERE id = :id"
            args = {"id": user}
        elif isinstance(user, str):
            query = "UPDATE users SET pw_bcrypt = :pw_bcrypt WHERE name_safe = :name_safe"
            args = {"name_safe": User.name_safe(user)}
        
        try:
            async with databases.Database(settings.DB_DSN) as db:
                await db.execute(query, {
                    **args,
                    "pw_bcrypt": bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                })
        except:
            return False
        finally:
            return True

    @staticmethod
    async def change_email(user: Union[int, str], email: str) -> bool:
        if isinstance(user, int):
            query = "UPDATE users SET email = :email WHERE id = :id"
            args = {"id": user}
        elif isinstance(user, str):
            query = "UPDATE users SET email = :email WHERE name_safe = :name_safe"
            args = {"name_safe": User.name_safe(user)}
        
        try:
            async with databases.Database(settings.DB_DSN) as db:
                await db.execute(query, {
                    **args,
                    "email": email
                })
        except:
            return False
        finally:
            return True
        
    @property
    def url(self) -> str:
        return f"https://undeniab.ly/{self.name}"