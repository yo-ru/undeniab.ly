from quart import Blueprint, render_template, redirect

home = Blueprint("home", __name__)

@home.route("/")
async def index_get():
    return redirect("/home")
    
@home.route("/home")
async def home_get():
    return await render_template("home.html")