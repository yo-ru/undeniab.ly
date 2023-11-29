from __future__ import annotations

from quart import Blueprint
from quart import render_template
from quart import request

from objects.user import User

store = Blueprint("store", __name__)


@store.route("/store")
async def store_get():
    return await render_template("store.html")
