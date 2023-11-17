import os
import aiohttp
import databases

from quart import Quart
from environs import Env

from cmyui import log, Ansi


# TODO: Actually write .env file ඞ
env = Env()
env.read_env()

app = Quart(__name__)

@app.before_serving
async def on_start():
    log("=== undeniab.ly ===", Ansi.LRED)
    log("Starting up... DONE", Ansi.LGREEN)
    
    # TODO: Database
    
    # TODO: Discord Integration
    
    # TODO: Probably some other shit
    
    log("===================", Ansi.LRED)
    
# home
from blueprints.home import home
app.register_blueprint(home)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8080)