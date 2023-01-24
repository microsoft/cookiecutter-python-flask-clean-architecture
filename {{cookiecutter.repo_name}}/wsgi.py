import logging
import sys

from src.app import app

logging.basicConfig(stream=sys.stderr)

if __name__ == "__main__":
    app.run()
