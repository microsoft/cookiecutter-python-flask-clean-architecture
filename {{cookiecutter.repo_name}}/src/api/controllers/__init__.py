from .todo import blueprint as todo_blueprint


def setup_blueprints(app) -> None:
    app.register_blueprint(todo_blueprint, url_prefix="/v1")
    return app


__all__ = ['setup_blueprints']
