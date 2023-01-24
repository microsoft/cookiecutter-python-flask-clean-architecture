from pathlib import Path

from flask_testing import TestCase
from testcontainers.postgres import PostgresContainer

from src import api
from src.config import Config
from src.create_app import create_app
from src.domain import SQLALCHEMY_DATABASE_URI

from src.infrastructure import sqlalchemy_db as db, setup_sqlalchemy


PROJECT_ROOT = str(Path(__file__).parent.parent.parent)


class AppTestBase(TestCase):

    def setup_database(self):
        self.postgres_container = PostgresContainer(image="postgres:14")
        self.postgres_container.start()
        self.app.config[SQLALCHEMY_DATABASE_URI] = \
            self.postgres_container.get_connection_url()
        setup_sqlalchemy(self.app)
        self.clear_database()

    def teardown_database(self):

        if self.postgres_container is not None:
            db.session.commit()
            db.session.close()
            self.postgres_container.stop()

    def clear_database(self):

        if self.postgres_container is not None:
            db.drop_all()
            db.create_all()

    def create_app(self):
        config = Config()
        config["TESTING"] = True
        app = create_app(config, dependency_container_packages=[api])
        return app

    def tearDown(self) -> None:
        self.teardown_database()
