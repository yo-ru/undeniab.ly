from quart import Blueprint, render_template, request

from objects.user import User

store = Blueprint("store", __name__)

@store.route("/store")
async def store_get(): 
    return await render_template("store.html")