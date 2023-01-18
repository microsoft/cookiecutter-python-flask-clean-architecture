# Cookie cutter template for a Python REST Api
This is a cookie cutter template for a Python REST Api. 
The application follows the Onion Architecture pattern. It uses SQLAlchemy 
for interacting with the database and Alembic for handling database migrations. 
Marshmallow is used for object serialization and deserialization. The 
application also supports maintenance windows for performing database 
migrations without disrupting the normal operation of the application.

Also, the application is dockerized and uses test containers for running the 
integration tests.

## Getting started
To start a new project, run the following command:
```bash
cookiecutter -c v1 https://github.com/drivendata/cookiecutter-data-science
```
This will prompt you for some information about your project. The information
you provide will be used to populate the files in the new project directory.

## Architecture 
The application follows the Onion Architecture pattern.
This architecture is a design pattern that organizes the codebase 
of a software application into multiple layers, where the innermost layer 
is the domain layer and the outermost layer is the application layer. 
Each layer depends only on the layers inside of it and not on the layers outside of it, 
creating a separation of concerns, allowing for a more maintainable and scalable codebase.

This architecture can be seen in the following diagram:
    
```
.
├── migrations
├── scripts
│   └── run_postgres.sh
├── src
│   ├── api
│   │   ├── controllers
│   │   │   └── ...  # controllers for the api
│   │   ├── schemas
│   │   │   └── ...  # Marshmallow schemas
│   │   ├── middleware.py
│   │   ├── responses.py
│   │   └── requests.py
│   ├── infrastructure
│   │   ├── services
│   │   │   └── ...  # Services that use third party libraries or services (e.g. email service)
│   │   ├── databases
│   │   │   └── ...  # Database adapaters and initialization
│   │   ├── repositories
│   │   │   └── ...  # Repositories for interacting with the databases
│   │   └── models
│   │   │   └── ...  # Database models
│   ├── domain
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── models
│   │   │   └── ...  # Business logic models
│   ├── services
│   │    └── ...  # Services for interacting with the domain (business logic)
│   ├── app.py
│   ├── config.py
│   ├── cors.py
│   ├── create_app.py
│   ├── dependency_container.py
│   ├── error_handler.py
│   └── logging.py
```
The application is structured with the following components:

* api (app) module: The outermost layer that contains the controllers and the endpoints definition, serialization and deserialization of the data, validation and error handling.
* infrastructure: Layer that typically include database connections, external APIs calls, logging and configuration management.
* services: Layer that contains the application's services, which encapsulate the core business logic and provide a higher-level abstraction for the application to interact with the domain entities.
* domain: The innermost layer that contains the core business logic and entities of the application.
* migrations: Alembic's migration scripts are stored here.
* scripts: contains the application's configuration settings.

## Database migrations
For performing database migrations during maintenance windows, 
you can use the manage.py command-line tool to generate and apply new migrations.

> Note: The application uses a postgres database. Make sure you have a postgres
> database running before running the following commands. For local development,
> you can use the run_postgres.sh script to run a postgres container locally.

```bash
# Generate a new migration
python manage.py db migrate -m "migration message"

# Apply the new migration
python manage.py db upgrade

# Downgrade the database to the previous migration
python manage.py db downgrade
```

## Tests
The application uses [python unittest] for unit testing for integration testing.

To run the unit tests, run the following command from the root directory:
```bash
python -m unittest discover -s tests
```

[python unittest]: https://docs.python.org/3/library/unittest.html