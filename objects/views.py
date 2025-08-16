from __future__ import annotations

import hashlib

import databases

import settings
from objects.user import User


class Views:
    def __init__(self, id: int, ip: str, country: str, user_id: int) -> None:
        self.id = id
        self.ip = ip
        self.country = country
        self.user_id = user_id

    @staticmethod
    async def from_user(user: User) -> list[Views]:
        async with databases.Database(settings.DB_DSN) as db:
            views = await db.fetch_all(
                "SELECT * FROM bio_views WHERE user_id = :user_id",
                {"user_id": user.id},
            )
            return [Views(**view) for view in views]

    @staticmethod
    async def add(ip: str, country: str, user_id: int) -> bool:
        async with databases.Database(settings.DB_DSN) as db:
            try:
                ip_hash = hashlib.sha256(ip.encode()).digest()
                await db.execute(
                    "INSERT INTO bio_views (ip, country, user_id) VALUES (:ip, :country, :user_id)",
                    {"ip": ip_hash, "country": country, "user_id": user_id},
                )
                return True
            except Exception:
                return False
