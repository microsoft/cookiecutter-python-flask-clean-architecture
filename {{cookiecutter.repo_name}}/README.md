# Cookiecutter actix simple clean architecture
This is a reusable Python Flask template. The project is based on Flask in combination with SQLAlchemy ORM.

Complete list of features the template provides:
* [Onion architecture](#onion-architecture)
* [Maintenance window support](#maintenance-window-support)
* [SQLAlchemy ORM](#sqlalchemy-orm)
* [Alembic Database migrations](#alembic-database-migrations)
* [Local postgres database docker support](#local-postgres-database-docker-support)
* [Test and test containers integration](#test-and-test-containers-integration)
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

## Onion Architecture 
The application follows the Onion Architecture pattern. An article is written 
about our experience integrating an onion architecture with actix web in combination with diesel ORM that can 
be found [here](./docs/onion-architecture-article.md).

This architecture is a design pattern that organizes the codebase of a software application into multiple layers, where the innermost layer 
is the domain layer and the outermost layer is the application layer. Each layer depends only on the layers inside of it and not on the layers outside of it, 
creating a separation of concerns, allowing for a more maintainable and scalable codebase.

For this template we suggest using a service-repository design pattern. For example implementations you can have a look at 


## Running the application locally
To run the application locally, you need to have a Postgres database running.
You can use the `run_postgres.sh` script in the `scripts` directory to run a Postgres container.
```bash
./scripts/run_postgres.sh
```

You can then run the application with flask:
```bash
Flask --app src/app run 
```
or with gunicorn:
```bash
gunicorn wsgi:app -b  0.0.0.0:7000 --workers=1 --preload
```

## Test and test containers integration
All tests are can be found under the `tests` folder. When using the template
you can place all you tests in this folder.

To run the tests, you can use the following command:
```bash
python -m unittest discover -s tests
```

## SQLAlchemy ORM
The template uses SQLAlchemy ORM for its database connection and database models
integration. Its is currently setup with postgres, however you can 
change it to any other database that is supported by diesel. For other databases 
have a look at the official Flask SQLAlchemy documentation that can be found [here](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)

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

## Tests
The application uses [python unittest] for unit testing for integration testing.

To run the unit tests, run the following command from the root directory:
```bash
python -m unittest discover -s tests
```

[python unittest]: https://docs.python.org/3/library/unittest.html

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

## Maintenance window support
TODO

## Dependency injection
TODO

## Test container integration

## Service repository design pattern

### SQLAlchemy Repositories
The onion architecture is best being used with a repository-service pattern. An example 
repository can be seen below:

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

### Services
The onion architecture is best being used with a repository-service pattern. An example 
service can be seen below:
```python
from services.repository_service import RepositoryService

class MyExampleService(RepositoryService):
    # The RepositoryService gives you access to crud repository operations by the inheritance 
    # RepositoryService.
    pass
```
