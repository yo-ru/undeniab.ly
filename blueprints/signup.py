from __future__ import annotations

from quart import Blueprint
from quart import render_template
from quart import request

import settings
from constants import regexes
from objects.user import User

signup = Blueprint("signup", __name__)


@signup.route("/signup")
async def signup_get():
    if User.authenticated():
        return (
            await render_template(
                "home.html",
                toast=("error", "You are already logged in."),
            ),
            403,
        )

    if not settings.REGISTRATION:
        return (
            await render_template(
                "home.html",
                toast=("error", "Registration is currently disabled."),
            ),
            401,
        )

    return await render_template("signup.html")


@signup.route("/signup", methods=["POST"])
async def signup_post():
    if User.authenticated():
        return (
            await render_template(
                "home.html",
                toast=("error", "You are already logged in."),
            ),
            403,
        )

    if not settings.REGISTRATION:
        return (
            await render_template(
                "home.html",
                toast=("error", "Registration is currently disabled."),
            ),
            401,
        )

    form = await request.form
    username = form.get("username")
    email = form.get("email")
    password = form.get("password")
    confirm_password = form.get("confirm-password")

    # Usernames must:
    # - be within 1-15 characters in length
    # - be alphanumeric
    # - not already be taken by another user
    if not 1 <= len(username) <= 32:
        return await render_template(
            "signup.html",
            toast=("error", "Username must be between 2 and 15 characters."),
        )

    if not username.isalnum():
        return await render_template(
            "signup.html",
            toast=("error", "Username must be alphanumeric."),
        )

    if not await User.available_name(username):
        return await render_template(
            "signup.html",
            toast=("error", "Username is already taken."),
        )

    # Emails must:
    # - match the regex `^[^@\s]{1,200}@[^@\s\.]{1,30}\.[^@\.\s]{1,24}$`
    # - not already be taken by another player
    if not regexes.email.match(email):
        return await render_template("signup.html", toast=("error", "Invalid email."))

    if not await User.available_email(email):
        return await render_template(
            "signup.html",
            toast=("error", "Email is already taken."),
        )

    # Passwords must:
    # - be within 8-32 characters in length
    # - have more than 3 unique characters
    # - password must match confirm password
    if not 8 <= len(password) <= 32:
        return await render_template(
            "signup.html",
            toast=("error", "Password must be between 8 and 32 characters."),
        )

    if len(set(password)) <= 3:
        return await render_template(
            "signup.html",
            toast=("error", "Password must have more than 3 unique characters."),
        )

    if password != confirm_password:
        return await render_template(
            "signup.html",
            toast=("error", "Passwords do not match."),
        )

    # add user to database and log them in
    await User.signup(username, email, password)
    return await render_template(
        "home.html",
        toast=("success", "Successfully signed up!"),
    )
