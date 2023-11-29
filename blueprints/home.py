from __future__ import annotations

from quart import Blueprint
from quart import redirect
from quart import render_template

home = Blueprint("home", __name__)


@home.route("/")
async def index_get():
    return redirect("/home")


@home.route("/home")
async def home_get():
    return await render_template("home.html")
