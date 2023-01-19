# Maintenance window strategy for database migrations
Database migrations can be a tricky task for any organization, especially when 
it comes to maintaining the availability of the system during the migration process. 
One way to mitigate this risk is to implement a maintenance window strategy.

A maintenance window is a specific time period during which a system or 
application is taken offline for maintenance or updates. This approach allows 
IT teams to perform necessary updates or migrations without affecting the 
availability of the system for end users or end up with a corrupt database.

As can be seen below in the diagram, the maintenance window strategy is
implemented by taking the system offline during the maintenance window and
performing the database migration. Once the migration is complete, the system
is brought back online. During the maintenance window, the system is not
available for end users and any requests made to the system receive a 503 
http status code.

<img src="./images/maintenance_window_sequence.jpg" alt="drawing" width="800"/>

The criteria for considering implementing a maintenance window strategy for database
migrations are:

* Your database does not have migration tools that can be used to perform migrations
  without taking the database offline.
* Your database is not hosted on a cloud provider that provides a managed database
  service that can be used to perform migrations without taking the database offline.

## Real world example
For a real world example, we will look at a maintenance window strategy implementation for
a FLASK application with a SQL based database. Given that the application uses SQLAlchemy and alembic for 
database migrations we will have the following components:

### Service context database model
The service context database model is a database model that is used to store the
current state of the service. This model is used to determine if the service is
in maintenance mode or not. The model is defined as follows:

> Note: The service context database model can also be extended to store other 
> information about the service such as the current version of the service.

```python
from src.infrastructure.databases import sqlalchemy_db as db
from src.infrastructure.models.model_extension import ModelExtension


class ServiceContext(db.Model, ModelExtension):
    __tablename__ = 'service_context'
    id = db.Column(db.Integer, primary_key=True)
    maintenance = db.Column(db.Boolean, default=False)
```

We use a database model to store the current state of the service because it allows
us to store the state of the service in a persistent manner. This means that if the
service is restarted, the state of the service will be restored. Also, if the service
is running on multiple instances, the state of the service will be consistent across
all instances. 

### Service context service
The service context service is a service that is used to interact with the service
context database model. The service context service is defined as follows:

```python
from src.infrastructure.models import ServiceContext
from src.infrastructure.databases import sqlalchemy_db as db


class ServiceContextService:

    def activate_maintenance_mode(self):
        status = ServiceContext.query.first()

        if status is None:
            status = ServiceContext()

        status.maintenance = True
        status.save(db)
        return status

    def deactivate_maintenance_mode(self):
        status = ServiceContext.query.first()

        if status is None:
            status = ServiceContext()

        status.maintenance = False
        status.save(db)
        return status

    def get_status(self):
        status = ServiceContext.query.first()

        if status is None:
            status = ServiceContext()
            status.save(db)

        return status
```

### Maintenance mode activation
To activate the maintenance mode, we can use a route as shown below:
```python
@blueprint.route('/maintenance/activate', methods=['GET'])
@inject
def activate_maintenance_mode(
    service_context_service=Provide[
        DependencyContainer.service_context_service
    ]
):
    service_context_service.activate_maintenance_mode()
    return jsonify({"message": "maintenance mode activated"}), 200
```
When creating a public route, make sure that you have a way to authenticate the user 
that makes the request in order to determine that the uses has the necessary permissions.

You can also create a management command with [Flask script]("https://flask-script.readthedocs.io/en/latest/") to 
activate the maintenance mode from within the application: 

```python
@manager.command
def activate_maintenance_mode():
    service_context_service = app.container.service_context_service()
    service_context_service.activate_maintenance_mode()
    logger.info("Maintenance mode activated")
```

### Maintenance mode deactivation
To deactivate the maintenance mode, we can use a route as shown below:
```python
@blueprint.route('/maintenance/deactivate', methods=['GET'])
@inject
def deactivate_maintenance_mode(
    service_context_service=Provide[
        DependencyContainer.service_context_service
    ]
):
    service_context_service.deactivate_maintenance_mode()
    return jsonify({"message": "maintenance mode deactivated"}), 200
```
Just as the activation mode, make sure that you have a way to authenticate the user
that makes the request in order to determine that the uses has the necessary permissions.

You can also create a management command with [Flask script]("https://flask-script.readthedocs.io/en/latest/") to
```python
@manager.command
def deactivate_maintenance_mode():
    service_context_service = app.container.service_context_service()
    service_context_service.deactivate_maintenance_mode()
    logger.info("Maintenance mode deactivated")
```

### Maintenance mode check
We're using the before_request decorator to run the maintenance mode check before
each request. The maintenance mode check is defined as follows:

```python
@app.before_request
def check_for_maintenance():
    service_context_service = app.container.service_context_service()
    status = service_context_service.get_status()

    if not ("maintenance" in request.path or "status" in request.path):
        if status.maintenance:
            return jsonify(
                {"message": "Service is currently enduring maintenance"}
            ), 503
```

With this implementation, the service will return a 503 http status code for all
requests that are not made to the maintenance mode activation, deactivation
or status routes.

## Applying migrations during maintenance window
You have several ways to apply migrations during a maintenance window. 

One way is to do the migration manually by running the migration commands from 
within the application. This is the simplest way to apply migrations and gives 
you the most control over the migration process.

An example of applying the migration manually is shown below in a kubernetes cluster:

1. Login into a pod that has access to a database and has the maintenance window strategy implemented
    ```bash
    kubectl exec -it <pod_name> -- /bin/bash
    ```

2. Activate the maintenance mode
    ```bash
    python manage.py activate_maintenance_mode
    ```

3. Apply the migration
    ```bash
    python manage.py db upgrade
    ```

4. Deactivate the maintenance mode
    ```bash
    python manage.py deactivate_maintenance_mode
    ```

## Closing remarks
When planning a maintenance window for a database migration, it's important to 
consider the following:

1) Identify the right time: Choose a time period that has the least impact on end users, such as during off-peak hours or weekends.

2) Communicate with stakeholders: Notify all stakeholders, including customers and internal teams, of the planned maintenance window well in advance. This will give them ample time to plan and prepare for the interruption in service.

3) Test the migration process: Before the actual migration, test the process in a non-production environment to ensure it runs smoothly. This will also help identify any potential issues that need to be addressed.

4) Have a rollback plan: In case something goes wrong during the migration, it's important to have a rollback plan in place to quickly restore the previous version of the database.

5) Monitor the migration: Continuously monitor the migration process to ensure it's running smoothly and to quickly address any issues that may arise.

6) By implementing a maintenance window strategy, organizations can minimize the impact of database migrations on end users and ensure the availability of the system during the migration process.

It's also important to note that some migrations such as those of a very large databases or 
those that require a lot of data transformation may require more than one maintenance window. 
In such scenarios it is important to plan and test the migration in chunks, allowing for a more 
gradual and controlled migration process.

Overall, a maintenance window strategy can be a useful tool for organizations looking to perform database migrations 
while minimizing disruption to end users. With careful planning, testing and monitoring, IT teams can ensure a 
smooth and successful migration process.