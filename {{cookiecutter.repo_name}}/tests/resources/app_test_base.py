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
    postgres_container = None

    def teardown_database(self):

        if self.postgres_container is not None:
            db.session.commit()
            db.session.close()
            self.postgres_container.stop()

    def initialize_database(self):

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def create_app(self):
        self.postgres_container = PostgresContainer(image="postgres:14")
        self.postgres_container.start()

        config = Config()
        config["TESTING"] = True
        config[SQLALCHEMY_DATABASE_URI] = \
            self.postgres_container.get_connection_url()

        self.app = create_app(
            config,
            dependency_container_packages=[api],
            setup_sqlalchemy=False
        )
        setup_sqlalchemy(self.app)
        self.initialize_database()
        return self.app

    def tearDown(self) -> None:
        self.teardown_database()
