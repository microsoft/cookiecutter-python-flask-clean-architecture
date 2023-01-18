import logging

from flask import Blueprint, jsonify
from dependency_injector.wiring import inject, Provide

from src.dependency_container import DependencyContainer
from src.api.responses import create_response
from src.api.schemas import ServiceContextSchema

logger = logging.getLogger(__name__)
blueprint = Blueprint('service_context', __name__)


@blueprint.route('/maintenance/activate', methods=['GET'])
@inject
def activate_maintenance_mode(
    service_context_service=Provide[
        DependencyContainer.service_context_service
    ]
):
    service_context_service.activate_maintenance_mode()
    return jsonify({"message": "maintenance mode activated"}), 200


@blueprint.route('/maintenance/deactivate', methods=['GET'])
@inject
def deactivate_maintenance_mode(
    service_context_service=Provide[
        DependencyContainer.service_context_service
    ]
):
    service_context_service.deactivate_maintenance_mode()
    return jsonify({"message": "maintenance mode deactivated"}), 200


@blueprint.route('/status', methods=['GET'])
@inject
def get_service_status(
    service_context_service=Provide[
        DependencyContainer.service_context_service
    ]
):
    status = service_context_service.get_status()
    return create_response(status, ServiceContextSchema)
