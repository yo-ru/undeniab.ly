from __future__ import annotations

from quart import Blueprint
from quart import render_template
from quart import request

from objects.bio import Bio
from objects.links import Links
from objects.user import User
from objects.views import Views

bio = Blueprint("bio", __name__)


@bio.route("/@<string:username>")
@bio.route("/<string:username>")
async def bio_get(username: str):
    user = await User.from_db(username)

    # user not found
    if not user:
        return await render_template("404.html"), 404

    # user is banned
    if user.is_banned():
        return await render_template("404.html"), 404

    # get bio
    bio = await Bio.from_user(user)

    # user is missing their bio table (shouldn't happen)
    if not bio:
        return (
            await render_template(
                "500.html",
                exception=Exception(f"{user.name} has no bio."),
            ),
            500,
        )

    # get links
    links = await Links.from_user(user)

    # add view
    await Views.add(
        ip=request.headers.get("CF-Connecting-IP"),
        country=request.headers.get("CF-IPCountry"),
        user_id=user.id,
    )

    # get views
    views = await Views.from_user(user)

    return await render_template(
        "bio.html",
        bio=bio,
        links=links,
        user=user,
        views=len(views),
    )
