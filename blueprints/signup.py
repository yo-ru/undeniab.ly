import bcrypt
import databases

from quart import Blueprint, render_template, request, session

from objects.user import User
from constants import regexes
import settings

signup = Blueprint("signup", __name__)

@signup.route("/signup")
async def signup_get():
    if "user" in session:
        return await render_template("home.html", toast=("error", "You are already logged in."))
    
    return await render_template("signup.html")

@signup.route("/signup", methods=["POST"])
async def signup_post():
    if "user" in session:
        return await render_template("home.html", toast=("error", "You are already logged in."))
    
    form = await request.form
    username = form.get("username")
    email = form.get("email")
    password = form.get("password")
    confirm_password = form.get("confirm-password")
    
    # Usernames must:
    # - be within 2-15 characters in length
    # - be alphanumeric
    # - not already be taken by another user
    if not 2 <= len(username) <= 32:
        return await render_template("signup.html", toast=("error", "Username must be between 2 and 15 characters."))
    
    if not username.isalnum():
        return await render_template("signup.html", toast=("error", "Username must be alphanumeric."))
    
    async with databases.Database(settings.DB_DSN) as db:
        if await db.fetch_one("SELECT 1 FROM users WHERE name_safe = :name_safe", {"name_safe": User.name_safe(username)}):
            return await render_template("signup.html", toast=("error", "Username is already taken."))
        
    # Emails must:
    # - match the regex `^[^@\s]{1,200}@[^@\s\.]{1,30}\.[^@\.\s]{1,24}$`
    # - not already be taken by another player
    if not regexes.email.match(email):
        return await render_template("signup.html", toast=("error", "Invalid email."))
    
    async with databases.Database(settings.DB_DSN) as db:
        if await db.fetch_one("SELECT 1 FROM users WHERE email = :email", {"email": email}):
            return await render_template("signup.html", toast=("error", "Email is already taken."))
        
    # Passwords must:
    # - be within 8-32 characters in length
    # - have more than 3 unique characters
    # - password must match confirm password
    if not 8 <= len(password) <= 32:
        return await render_template("signup.html", toast=("error", "Password must be between 8 and 32 characters."))
    
    if len(set(password)) <= 3:
        return await render_template("signup.html", toast=("error", "Password must have more than 3 unique characters."))
    
    if password != confirm_password:
        return await render_template("signup.html", toast=("error", "Passwords do not match."))
    
    pw_bcrypt = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    # add user to database and log them in
    await User.signup(username, email, pw_bcrypt)
    return await render_template("home.html", toast=("success", "Successfully signed up!"))
    