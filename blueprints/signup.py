from quart import Blueprint, render_template

signup = Blueprint("signup", __name__)

@signup.route("/signup")
async def signup_get():
    return await render_template("signup.html")