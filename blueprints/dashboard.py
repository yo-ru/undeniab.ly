from __future__ import annotations

from quart import Blueprint
from quart import render_template

from objects.user import User

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("")
@dashboard.route("/")
async def home_get():
    if not User.authenticated():
        return await render_template(
            "login.html",
            toast=("error", "You are not logged in."),
        )

    return await render_template("dashboard/home.html")


@dashboard.route("/account")
async def account_get():
    if not User.authenticated():
        return await render_template(
            "login.html",
            toast=("error", "You are not logged in."),
        )

    return await render_template("dashboard/account.html")


@dashboard.route("/bio")
async def bio_get():
    if not User.authenticated():
        return await render_template(
            "login.html",
            toast=("error", "You are not logged in."),
        )

    return await render_template("dashboard/bio.html")


@dashboard.route("/domains")
async def domains_get():
    if not User.authenticated():
        return await render_template(
            "login.html",
            toast=("error", "You are not logged in."),
        )

    return await render_template("dashboard/domains.html")


@dashboard.route("/settings")
async def settings_get():
    if not User.authenticated():
        return await render_template(
            "login.html",
            toast=("error", "You are not logged in."),
        )

    return await render_template("dashboard/settings.html")
