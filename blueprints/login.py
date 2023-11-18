from quart import Blueprint, render_template

login = Blueprint("login", __name__)

@login.route("/login")
async def login_get():
    return await render_template("login.html")