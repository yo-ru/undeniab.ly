import os
import databases

from cmyui import log, Ansi
from quart import Quart, render_template
from werkzeug.exceptions import HTTPException

from objects.user import User
from constants.privileges import Privileges

import settings

# app
app = Quart(__name__)
app.secret_key = settings.QUART_SECRET

# expose objects to jinja
exposed_objects = {
    "User": User,
    "Privileges": Privileges
}
for obj in exposed_objects:
    app.jinja_env.globals[obj] = exposed_objects[obj]

# before serving
@app.before_serving
async def on_start():
    log("=== undeniab.ly ===", Ansi.LRED)
    
    # Check database connection
    try:
        log(f"Connecting to database...", Ansi.LGREEN)
        db = databases.Database(settings.DB_DSN)
        await db.connect()
        await db.disconnect()
    except Exception as e:
        log(f"Failed to connect to database: {e}", Ansi.LRED)
        log("===================", Ansi.LRED)
        os._exit(1)
    
    log("===================", Ansi.LRED)

# register blueprints
from blueprints.home import home
app.register_blueprint(home)

from blueprints.store import store
app.register_blueprint(store)

from blueprints.login import login
app.register_blueprint(login)

from blueprints.signup import signup
app.register_blueprint(signup)

from blueprints.logout import logout
app.register_blueprint(logout)

from blueprints.dashboard import dashboard
app.register_blueprint(dashboard, url_prefix="/dashboard")

# error handling
@app.errorhandler(Exception)
async def handle_exception(exception):
    # 404
    if isinstance(exception, HTTPException):
        if exception.code == 404:
            return await render_template("404.html"), 404
    
    # 5XX
    log(f"Unhandled exception: {exception}", Ansi.LRED)
    return await render_template("500.html", exception=exception), 500

# run
if __name__ == "__main__":
    app.run(debug=settings.QUART_DEBUG, host=settings.QUART_HOST, port=settings.QUART_PORT)