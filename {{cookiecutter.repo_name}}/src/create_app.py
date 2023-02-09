from flask import Flask

from src import api
from src.api import setup_prefix_middleware, setup_blueprints
from src.cors import setup_cors
from src.dependency_container import setup_dependency_container
from src.error_handler import setup_error_handler
from src.infrastructure import setup_sqlalchemy
from src.logging import setup_logging
from src.domain import SERVICE_PREFIX
from src.management import setup_management


def create_app(
    config,
    dependency_container_packages=None,
    dependency_container_modules=None,
):
    app = Flask(__name__.split('.')[0])
    app = setup_logging(app)
    app.config.from_object(config)
    app = setup_dependency_container(app)
    app.container.wire(packages=[api])
    app = setup_cors(app)
    app.url_map.strict_slashes = False
    app = setup_prefix_middleware(app, prefix=app.config[SERVICE_PREFIX])
    app = setup_blueprints(app)
    app = setup_sqlalchemy(app)
    app = setup_error_handler(app)
    app = setup_management(app)

    # Dependency injection container initialization should be done last
    app = setup_dependency_container(
        app,
        packages=dependency_container_packages,
        modules=dependency_container_modules
    )
    return app
