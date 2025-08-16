from __future__ import annotations

import databases

import settings
from objects.user import User


class Bio:
    def __init__(
        self,
        id: int,
        user_id: int,
        display_name: str,
        display_name_sparkle: bool,
        display_name_sparkle_color: str,
        description: str,
        typing_description: str,
        pfp_url: str,
        use_discord_pfp: bool,
        pfp_decoration: str,
        banner_url: str,
        bg_url: str,
        bg_color: str,
        bg_blur: int,
        bg_brightness: int,
        autoplay_fix: bool,
        autoplay_txt: str,
        media_embed_title: str,
        media_embed_url: str,
        media_embed_default_open: bool,
        cursor_url: str,
        cursor_center: bool,
        cursor_effect: str,
        animate_title: bool,
        p_color: str,
        s_color: str,
        a_color: str,
        t_color: str,
        i_color: str,
        font: str,
        opacity: int,
        blur: int,
        border_width: int,
        border_radius: int,
        show_views: bool,
        show_badges: bool,
        badge_position: str,
        glow: bool,
        rounded_socials: bool,
        animations: bool,
        parallex: bool,
        discord_presence: bool,
        discord_invite: str,
        show_custom_link_url: bool,
        layout: str,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.display_name = display_name
        self.display_name_sparkle = display_name_sparkle
        self.display_name_sparkle_color = display_name_sparkle_color
        self.description = description
        self.typing_description = typing_description
        self.pfp_url = pfp_url
        self.use_discord_pfp = use_discord_pfp
        self.pfp_decoration = pfp_decoration
        self.banner_url = banner_url
        self.bg_url = bg_url
        self.bg_color = bg_color
        self.bg_blur = bg_blur
        self.bg_brightness = bg_brightness
        self.autoplay_fix = autoplay_fix
        self.autoplay_txt = autoplay_txt
        self.media_embed_title = media_embed_title
        self.media_embed_url = media_embed_url
        self.media_embed_default_open = media_embed_default_open
        self.cursor_url = cursor_url
        self.cursor_center = cursor_center
        self.cursor_effect = cursor_effect
        self.animate_title = animate_title
        self.p_color = p_color
        self.s_color = s_color
        self.a_color = a_color
        self.t_color = t_color
        self.i_color = i_color
        self.font = font
        self.opacity = opacity
        self.blur = blur
        self.border_width = border_width
        self.border_radius = border_radius
        self.show_views = show_views
        self.show_badges = show_badges
        self.badge_position = badge_position
        self.glow = glow
        self.rounded_socials = rounded_socials
        self.animations = animations
        self.parallex = parallex
        self.discord_presence = discord_presence
        self.discord_invite = discord_invite
        self.show_custom_link_url = show_custom_link_url
        self.layout = layout

    @staticmethod
    async def from_db(user: int | str) -> Bio:
        if isinstance(user, int):
            query = "SELECT bio_settings.* FROM bio_settings JOIN users ON bio_settings.user_id = users.id WHERE bio_settings.user_id = :user_id"
            args = {"user_id": user}
        elif isinstance(user, str):
            query = "SELECT bio_settings.* FROM bio_settings JOIN users ON bio_settings.user_id = users.id WHERE users.name_safe = :name_safe"
            args = {"name_safe": User.name_safe(user)}

        async with databases.Database(settings.DB_DSN) as db:
            bio_db = await db.fetch_one(query, args)
            if bio_db is None:
                return None
            return Bio(**bio_db)

    @staticmethod
    async def from_user(user: User) -> Bio:
        return await Bio.from_db(user.id)
