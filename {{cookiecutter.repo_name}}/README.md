# Cookiecutter flask clean architecture
This is a reusable Python Flask template. The project is based on Flask in combination with SQLAlchemy ORM.

Complete list of features the template provides:
* [Onion architecture](#onion-architecture)
* [Maintenance window support](#maintenance-window-support)
* [SQLAlchemy ORM](#sqlalchemy-orm)
* [Alembic Database migrations](#alembic-database-migrations)
* [Local postgres database docker support](#local-postgres-database-docker-support)
* [Tests and test containers integration](#tests-and-test-containers-integration)
* [Service prefix](#service-prefix)
* [Dependency injection](#dependency-injection)
* [Service-repository design pattern](#service-repository-design-pattern)

## Getting started
To start a new project, run the following command:
```bash
cookiecutter -c v1 https://github.com/microsoft/cookiecutter-python-flask-clean-architecture
```
This will prompt you for some information about your project. The information
you provide will be used to populate the files in the new project directory.

### Running the application locally
To run the application locally, you need to have a Postgres database running.
You can use the `run_postgres.sh` script in the `scripts` directory to run a Postgres container.
```bash
./scripts/run_postgres.sh
```
You can then run the application with flask:
```bash
flask --app src/app run 
```
or with gunicorn:
```bash
gunicorn wsgi:app -b  0.0.0.0:7000 --workers=1 --preload
```

## Onion Architecture 
The application follows the Onion Architecture pattern. An article is written 
about our experience integrating an onion architecture with flask in combination with 
SQL Alchemy ORM that can be found [here](./docs/onion-architecture-article.md).

This architecture is a design pattern that organizes the codebase of a software application into multiple layers, where the innermost layer 
is the domain layer and the outermost layer is the application layer. Each layer depends only on the layers inside of it and not on the layers outside of it, 
creating a separation of concerns, allowing for a more maintainable and scalable codebase.

For this template we suggest using a service-repository design pattern. This template also provides 
a set of abc meta classes that you can use to create your repositories and services.
For example implementations you can have a look at [Service-repository design pattern](#service-repository-design-pattern).

## Maintenance window support
This template provides you with a maintenance window mode. To learn more about 
maintenance windows in your service you can read this article [here](https://devblogs.microsoft.com/cse/2023/02/08/maintenance_window_db_migrations/)

During maintenance mode, clients will receive an http 503 status code.

### Activating maintenance mode
You can activate maintenance mode in the following ways:
```bash
curl -X PATCH http://localhost:7000/<service-prefix>/v1/service-context -d '{"maintenance": true}' -H 'Content-Type: application/json'
```
or via the command line:
```bash
flask activate_maintenance_mode
```

### Deactivating maintenance mode
You can deactivate maintenance mode in the following ways:
```bash
curl -X PATCH http://localhost:7000/<service-prefix>/v1/service-context -d '{"maintenance": false}' -H 'Content-Type: application/json'
```
or via the command line:
```bash
flask deactivate_maintenance_mode
```

## SQLAlchemy ORM
The template uses SQLAlchemy ORM for its database connection and database models
integration. Its is currently setup with postgres, however you can 
change it to any other database that is supported by SQLAlchemy. For other databases 
have a look at the official Flask SQLAlchemy documentation 
that can be found [here](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)

This template provides you with a model base class that you can use to create your models.

```python
from src.infrastructure.models.model_extension import ModelExtension

class User(ModelExtension):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    attribute_a = Column(String(50), nullable=False)
    attribute_b = Column(String(50), nullable=False)

    def __repr__(self):
        return self.repr(id=self.id, attribute_a=self.attribute_a, attribute_b=self.attribute_b)
```

## Alembic database migrations
> Note: The application uses a postgres database. Make sure you have a postgres
> database running before running the following commands. For local development,
> you can use the run_postgres.sh script to run a postgres container locally.

1) Make sure you have the diesel cli installed. You can install it with the following command:
    ```bash
    sh ./scripts/run_postgres.sh
    ```
2) Create a database migration
    ```bash
    flask db migrate -m <migration-message>
    ```
3) Apply the database migration:
    ```bash
    flask db upgrade
    ```
   
## Local postgres database docker support 
You can run a local postgres docker database by using the following script:
```bash
 sh ./scripts/run_postgres.sh
 ```

This will run a postgres docker container on port 5432. Also it will create a
.env file in the root directory of the project. This file contains the database
connection string. The service will read this connection string from the .env file 
and use it to connect to the database.

## Tests and test containers integration
All tests are can be found under the `tests` folder. When using the template
you can place all you tests in this folder.

The service uses [python unittest](https://docs.python.org/3/library/unittest.html) in combination
with [flask testing]

To run the tests, you can use the following command:
```bash
python -m unittest discover -s tests
```

You can use the test containers library to run your tests against a postgres database.
You do this by ```setup_database()``` in your test class. This will create a postgres container
and run your tests against it. After the tests are done, the container will be destroyed.

If you want to run your tests against a different database, you can change the 
setyp_database method in the test class to use a different database container.

```python
class Test(AppTestBase):

    def setUp(self) -> None:
        super(Test, self).setUp()
        self.setup_database()
```

## Service prefix
The application can use a service prefix for the endpoints.
The service prefix is defined in the config.py file. Given a service prefix 
of 'example', endpoints will be prefixed with '/example/v1/service-context'.

```python
# config.py
SERVICE_PREFIX = os.environ.get(SERVICE_PREFIX, '')

# middleware
class PrefixMiddleware(object):
    ROUTE_NOT_FOUND_MESSAGE = "This url does not belong to the app."

    def __init__(self, app, prefix=''):
        self.app = app
        self.wsgi_app = app.wsgi_app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.wsgi_app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return [self.ROUTE_NOT_FOUND_MESSAGE.encode()]
```

During testing the service prefix is not applied. This allows you
to test the endpoints without having to add the service prefix to the
endpoint.

If the service prefix is not set, the service will not use a service prefix.


## Dependency injection
This template uses the [dependency_injector](https://pypi.org/project/dependency-injector/) library
for dependency injection. The template provides you with a container class that you can use to
register your dependencies. The container class is located in the `src/dependency_container.py` file.

You can add your dependencies to the container and use them 
in your routers, services and repositories.

## Service repository design pattern
This template provides you with a repository-service pattern. There are two base classes
that you can use to create your repositories and services. These base classes are located
in the `src/services/repository_service.py` and `src/infrastructure/repositories/repository.py`.

### Repository example
A repository example can be seen below, this repository is used to query the MyModel model.
For custom query params support override the `_apply_query_params` method.

```python
from infrastructure.repositories import Repository
from infrastructure.models import MyModel

class MyExampleRepository(Repository):
    base_class = MyModel
    DEFAULT_NOT_FOUND_MESSAGE = "MyModel was not found"

    def _apply_query_params(self, query, query_params):
        name_query_param = self.get_query_param("name", query_params)
        
        if name_query_param:
           query = query.filter_by(name=name_query_param)
            
        return query
```

### Service example
A Service example can be seen below, this service expect a repository to be injected in its contuctor.

```python
from services.repository_service import RepositoryService

class MyExampleService(RepositoryService):
    # The RepositoryService gives you access to crud repository operations by the inheritance 
    # RepositoryService.
    pass

# Can be instantiate by injecting the repository
my_example_service = MyExampleService(my_example_repository)
```
