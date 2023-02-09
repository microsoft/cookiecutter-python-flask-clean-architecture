import logging

from flask_migrate import Migrate
from src.infrastructure import sqlalchemy_db as db

migrate = Migrate()
logger = logging.getLogger(__name__)


def setup_management(app):
    migrate.init_app(app, db)

    @app.cli.command("show_db_tables")
    def show_db_tables():
        print(db.engine.table_names())

    @app.cli.command("print_config")
    def print_config():
        print(app.config)

    @app.cli.command("activate_maintenance_mode")
    def activate_maintenance_mode():
        service_context_service = app.container.service_context_service()
        service_context_service.update({"maintenance": True})
        logger.info("Maintenance mode activated")

    @app.cli.command("deactivate_maintenance_mode")
    def deactivate_maintenance_mode():
        service_context_service = app.container.service_context_service()
        service_context_service.update({"maintenance": False})
        logger.info("Maintenance mode deactivated")

    return app
