from __future__ import annotations

from typing import Any
from typing import Union

import bcrypt
import databases
from cmyui import Ansi
from cmyui import log
from quart import session

import settings
from constants.privileges import Privileges


class User:
    def __init__(
        self,
        id: int,
        name: str,
        email: str,
        privileges: int,
        badges: int,
    ) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.privileges = privileges
        self.badges = badges

    def __repr__(self) -> str:
        return f"<{self.name} ({self.id})>"

    @staticmethod
    def from_dict(user: dict[str, Any]) -> User:
        return User(**user)

    @staticmethod
    async def from_db(user: int | str) -> User | None:
        # check if user is int or str
        if isinstance(user, int):
            query = "SELECT id, name, email, privileges, badges FROM users WHERE id = :id"
            args = {"id": user}
        elif isinstance(user, str):
            query = "SELECT id, name, email, privileges, badges FROM users WHERE name_safe = :name_safe"
            args = {"name_safe": User.name_safe(user)}

        async with databases.Database(settings.DB_DSN) as db:
            user_db = await db.fetch_one(query, args)

            if user_db:
                return User(**user_db)
            return None

    @staticmethod
    def name_safe(name: str) -> str:
        return name.lower().replace(" ", "_")

    @staticmethod
    async def signup(name: str, email: str, password: str) -> None:
        async with databases.Database(settings.DB_DSN) as db:
            await db.execute(
                "INSERT INTO users (name, name_safe, email, pw_bcrypt) VALUES (:name, :name_safe, :email, :pw_bcrypt)",
                {
                    "name": name,
                    "name_safe": User.name_safe(name),
                    "email": email,
                    "pw_bcrypt": bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
                },
            )

            user = await User.from_db(name)
            
            # Create default bio settings for the new user
            await User._create_default_bio_settings(user.id)
            
            session["user"] = user.__dict__
            log(f"{user} has signed up!", Ansi.LGREEN)

    @staticmethod
    async def _create_default_bio_settings(user_id: int) -> None:
        """Create default bio settings for a new user."""
        async with databases.Database(settings.DB_DSN) as db:
            await db.execute(
                """INSERT INTO bio_settings (
                    user_id, display_name, display_name_sparkle, display_name_sparkle_color,
                    description, typing_description, pfp_url, use_discord_pfp, pfp_decoration,
                    banner_url, bg_url, bg_color, bg_blur, bg_brightness, autoplay_fix,
                    autoplay_txt, media_embed_title, media_embed_url, media_embed_default_open,
                    cursor_url, cursor_center, cursor_effect, animate_title, p_color, s_color,
                    a_color, t_color, i_color, font, opacity, blur, border_width, border_radius,
                    show_views, show_badges, badge_position, glow, rounded_socials, animations,
                    parallex, discord_presence, discord_invite, show_custom_link_url, layout
                ) VALUES (
                    :user_id, :display_name, :display_name_sparkle, :display_name_sparkle_color,
                    :description, :typing_description, :pfp_url, :use_discord_pfp, :pfp_decoration,
                    :banner_url, :bg_url, :bg_color, :bg_blur, :bg_brightness, :autoplay_fix,
                    :autoplay_txt, :media_embed_title, :media_embed_url, :media_embed_default_open,
                    :cursor_url, :cursor_center, :cursor_effect, :animate_title, :p_color, :s_color,
                    :a_color, :t_color, :i_color, :font, :opacity, :blur, :border_width, :border_radius,
                    :show_views, :show_badges, :badge_position, :glow, :rounded_socials, :animations,
                    :parallex, :discord_presence, :discord_invite, :show_custom_link_url, :layout
                )""",
                {
                    "user_id": user_id,
                    "display_name": "",
                    "display_name_sparkle": 0,
                    "display_name_sparkle_color": 16347926,
                    "description": "",
                    "typing_description": 0,
                    "pfp_url": "",
                    "use_discord_pfp": 0,
                    "pfp_decoration": 0,
                    "banner_url": "",
                    "bg_url": "",
                    "bg_color": 1579035,
                    "bg_blur": 0,
                    "bg_brightness": 100,
                    "autoplay_fix": 0,
                    "autoplay_txt": "click anywhere",
                    "media_embed_title": "",
                    "media_embed_url": "",
                    "media_embed_default_open": 0,
                    "cursor_url": "",
                    "cursor_center": 0,
                    "cursor_effect": "sparkle",
                    "animate_title": 0,
                    "p_color": 1579035,
                    "s_color": 1579035,
                    "a_color": 16347926,
                    "t_color": 16347926,
                    "i_color": 16347926,
                    "font": "Fira Code",
                    "opacity": 0.6,
                    "blur": 10,
                    "border_width": 2,
                    "border_radius": 0.4,
                    "show_views": 1,
                    "show_badges": 1,
                    "badge_position": "corner",
                    "glow": 0,
                    "rounded_socials": 1,
                    "animations": 0,
                    "parallex": 1,
                    "discord_presence": 1,
                    "discord_invite": "",
                    "show_custom_link_url": 1,
                    "layout": 1
                }
            )

    @staticmethod
    async def login(name: str, password: str) -> bool:
        async with databases.Database(settings.DB_DSN) as db:
            # NOTE: we avoid using User.from_db here because we don't want to store the password in the session
            user_db = await db.fetch_one(
                "SELECT id, name, email, privileges, badges, pw_bcrypt FROM users WHERE name_safe = :name_safe",
                {"name_safe": User.name_safe(name)},
            )

            if user_db and bcrypt.checkpw(
                password.encode(),
                user_db["pw_bcrypt"].encode(),
            ):
                user = User(user_db.id, user_db.name, user_db.email, user_db.privileges, user_db.badges)
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
        return User.from_dict(session["user"]).privileges & privilege

    @staticmethod
    async def available_name(name: str) -> bool:
        async with databases.Database(settings.DB_DSN) as db:
            return not await db.fetch_one(
                "SELECT 1 FROM users WHERE name_safe = :name_safe",
                {"name_safe": User.name_safe(name)},
            )

    @staticmethod
    async def available_email(email: str) -> bool:
        async with databases.Database(settings.DB_DSN) as db:
            return not await db.fetch_one(
                "SELECT 1 FROM users WHERE email = :email",
                {"email": email},
            )

    @staticmethod
    async def change_password(user: int | str, password: str) -> bool:
        if isinstance(user, int):
            query = "UPDATE users SET pw_bcrypt = :pw_bcrypt WHERE id = :id"
            args = {"id": user}
        elif isinstance(user, str):
            query = (
                "UPDATE users SET pw_bcrypt = :pw_bcrypt WHERE name_safe = :name_safe"
            )
            args = {"name_safe": User.name_safe(user)}

        try:
            async with databases.Database(settings.DB_DSN) as db:
                await db.execute(
                    query,
                    {
                        **args,
                        "pw_bcrypt": bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
                    },
                )
        except:
            return False
        finally:
            return True

    @staticmethod
    async def change_email(user: int | str, email: str) -> bool:
        if isinstance(user, int):
            query = "UPDATE users SET email = :email WHERE id = :id"
            args = {"id": user}
        elif isinstance(user, str):
            query = "UPDATE users SET email = :email WHERE name_safe = :name_safe"
            args = {"name_safe": User.name_safe(user)}

        try:
            async with databases.Database(settings.DB_DSN) as db:
                await db.execute(query, {**args, "email": email})
        except:
            return False
        finally:
            return True

    @staticmethod
    def is_banned() -> bool:
        if not User.authenticated():
            return False
        return User.from_dict(session["user"]).privileges & Privileges.UNBANNED == 0

    @property
    def url(self) -> str:
        return f"https://undeniab.ly/{self.name}"
