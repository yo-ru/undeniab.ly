import os
import databases

from quart import Quart
from cmyui import log, Ansi

import settings

app = Quart(__name__)

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
    
    # TODO: Probably some other shit
    
    log("===================", Ansi.LRED)
    
# home
from blueprints.home import home
app.register_blueprint(home)

# login
from blueprints.login import login
app.register_blueprint(login)

# signup
from blueprints.signup import signup
app.register_blueprint(signup)

if __name__ == "__main__":
    app.run(debug=settings.QUART_DEBUG, host=settings.QUART_HOST, port=settings.QUART_PORT)