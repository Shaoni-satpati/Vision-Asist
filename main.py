import os
from dotenv import load_dotenv
load_dotenv()                      # load .env before importing config

from config import config
from server.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(
        host  = config.SERVER_HOST,
        port  = config.SERVER_PORT,
        debug = config.DEBUG,
    )
