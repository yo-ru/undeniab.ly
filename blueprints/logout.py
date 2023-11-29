from __future__ import annotations

from quart import Blueprint
from quart import render_template

from objects.user import User

logout = Blueprint("logout", __name__)


@logout.route("/logout")
async def logout_get():
    if not User.authenticated():
        return await render_template(
            "login.html", toast=("error", "You are not logged in."),
        )

    User.logout()

    return await render_template(
        "login.html", toast=("success", "Successfully logged out!"),
    )
