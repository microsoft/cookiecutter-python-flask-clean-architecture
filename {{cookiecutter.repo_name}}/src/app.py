import logging

from flask import request, jsonify

from src.create_app import create_app
from src.config import Config
from src import api


logger = logging.getLogger(__name__)
app = create_app(Config, dependency_container_packages=[api])


@app.before_request
def check_for_maintenance():
    service_context_service = app.container.service_context_service()
    status = service_context_service.get_service_context()

    if not ("maintenance" in request.path or "status" in request.path):
        if status.maintenance:
            return jsonify(
                {"message": "Service is currently enduring maintenance"}
            ), 503


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)
