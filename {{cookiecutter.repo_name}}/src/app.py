import logging
import os

from src.create_app import create_app
from src.config import Config
from src import api



logger = logging.getLogger(__name__)
app = create_app(Config, dependency_container_packages=[api])


if __name__ == '__main__':
    app_env = os.getenv('FLASK_ENV', 'development')
    port = os.getenv('PORT', 7000)
    debug = True

    if app_env != 'development':
        debug = True

    app.run(debug=debug, host='0.0.0.0', port=port)
