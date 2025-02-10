from dependency_injector import containers, providers

from src.infrastructure import SQLTodoRepository
from src.services import TodoService


def setup_dependency_container(app, modules=None, packages=None):
    container = DependencyContainer()
    app.container = container
    app.container.wire(modules=modules, packages=packages)
    return app


class DependencyContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration()
    todo_repository = providers.Factory(SQLTodoRepository)
    todo_service = providers.Factory(
        TodoService, repository=todo_repository,
    )
