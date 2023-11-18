from quart import Blueprint, render_template, request, session

from objects.user import User

login = Blueprint("login", __name__)

@login.route("/login")
async def login_get():
    if "user" in session:
        return await render_template("home.html", toast=("error", "You are already logged in."))
    
    return await render_template("login.html")

@login.route("/login", methods=["POST"])
async def login_post():
    if "user" in session:
        return await render_template("home.html", toast=("error", "You are already logged in."))
    
    form = await request.form
    username = form.get("username")
    password = form.get("password")
    
    if await User.login(username, password):
        session["user"] = (await User.login(username, password)).__dict__
        return await render_template("home.html", toast=("success", "Successfully logged in!"))
    
    return await render_template("login.html", toast=("error", "Invalid username or password."))