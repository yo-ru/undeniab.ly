from quart import Blueprint, render_template, session

logout = Blueprint("logout", __name__)

@logout.route("/logout")
async def logout_get():
    if "user" not in session:
        return await render_template("login.html", toast=("error", "You are not logged in."))
    
    session.pop("user", None)
    
    return await render_template("home.html", toast=("success", "Successfully logged out!"))