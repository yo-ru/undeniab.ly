from __future__ import annotations

from quart import Blueprint
from quart import render_template
from quart import request

from objects.user import User
from objects.bio import Bio
from objects.links import Links

bio = Blueprint("bio", __name__)

@bio.route("/@<string:username>")
@bio.route("/<string:username>")
async def bio_get(username: str):
    user = await User.from_db(username)
    
    if not user:
        return await render_template("404.html"), 404

    if user.is_banned():
        return await render_template("404.html"), 404

    bio = await Bio.from_user(user)

    # user is missing their bio table (shouldn't happen)
    if not bio:
        return await render_template("500.html", exception=Exception(f"{user.name} has no bio.")), 500

    links = await Links.from_user(user)

    return await render_template("bio.html", bio=bio, privileges=user.privileges, badges=user.badges, links=links)