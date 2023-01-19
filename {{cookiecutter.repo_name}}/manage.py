import logging

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from src.config import Config
from src.create_app import create_app
from src.infrastructure import sqlalchemy_db as db

app = create_app(Config, dependency_container_modules=["manage"])
migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
logger = logging.getLogger(__name__)


@manager.command
def show_config():
    print(app.config)


@manager.command
def show_db_tables():
    print(db.engine.table_names())


@manager.command
def activate_maintenance_mode():
    service_context_service = app.container.service_context_service()
    service_context_service.activate_maintenance_mode()
    logger.info("Maintenance mode activated")


@manager.command
def deactivate_maintenance_mode():
    service_context_service = app.container.service_context_service()
    service_context_service.deactivate_maintenance_mode()
    logger.info("Maintenance mode deactivated")


@manager.command
def remove_alembic_versions_table():
    connection = db.engine.raw_connection()
    cursor = connection.cursor()
    command = "DROP TABLE IF EXISTS alembic_version;"
    cursor.execute(command)
    connection.commit()
    cursor.close()
    print("alembic_version table removed")
