from __future__ import annotations

import databases

import settings
from objects.user import User

class Links:
    def __init__(
        self,
        id: int,
        user_id: int,
        link_id: int,
        link_parent_id: int,
        link_platform: str,
        link_url: str,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.link_id = link_id
        self.link_parent_id = link_parent_id
        self.link_platform = link_platform
        self.link_url = link_url

    def __repr__(self) -> str:
        return f"<{self.link_platform} ({self.link_url})>"

    @staticmethod
    async def from_user(user: User) -> list[Links]:
        async with databases.Database(settings.DB_DSN) as db:
            links = await db.fetch_all(
                "SELECT * FROM bio_links WHERE user_id = :user_id",
                {"user_id": user.id},
            )

            # sort links by link_id (first id is always null) and link_parent_id
            links.sort(key=lambda x: (x.link_id, x.link_parent_id))
            return [Links(**link) for link in links]