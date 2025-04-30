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
    initialize_database=True
):
    """
    Factory function to create a Flask application instance.

    Args:
        config (object): Configuration object for the Flask app.
        dependency_container_modules (list): List of modules to
            wire with the dependency container. Defaults to None.
        setup_sqlalchemy (bool): Flag to set up SQLAlchemy.
            Defaults to True.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)

    # Setup logging should be run after the config is loaded
    app = setup_logging(app)
    app = setup_dependency_container(app)
    app.container.wire(packages=[api])
    app = setup_cors(app)
    app.url_map.strict_slashes = False
    app = setup_prefix_middleware(app, prefix=app.config[SERVICE_PREFIX])
    app = setup_blueprints(app)

    if initialize_database:
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
