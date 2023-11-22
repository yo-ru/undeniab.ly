from quart import Blueprint, render_template, request

from objects.user import User

login = Blueprint("login", __name__)

@login.route("/login")
async def login_get():
    if User.authenticated():
        return await render_template("home.html", toast=("error", "You are already logged in.")), 403
    
    return await render_template("login.html")

@login.route("/login", methods=["POST"])
async def login_post():
    if User.authenticated():
        return await render_template("home.html", toast=("error", "You are already logged in.")), 403
    
    form = await request.form
    username = form.get("username")
    password = form.get("password")
    
    if await User.login(username, password):
        return await render_template("home.html", toast=("success", "Successfully logged in!"))
    
    return await render_template("login.html", toast=("error", "Invalid username or password."))