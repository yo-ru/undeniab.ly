from __future__ import annotations

from quart import Blueprint
from quart import render_template

from objects.user import User

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
async def home_get():
    if not User.authenticated():
        return await render_template(
            "login.html", toast=("error", "You are not logged in."),
        )

    return await render_template("dashboard/home.html")
