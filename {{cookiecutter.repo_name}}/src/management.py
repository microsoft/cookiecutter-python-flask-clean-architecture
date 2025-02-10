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

    return app
