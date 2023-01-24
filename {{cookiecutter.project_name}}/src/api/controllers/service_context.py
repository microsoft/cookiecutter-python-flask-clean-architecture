import logging

from dependency_injector.wiring import inject, Provide
from flask import Blueprint

from src.api.middleware import post_data_required
from src.api.responses import create_response
from src.api.schemas import ServiceContextSchema
from src.dependency_container import DependencyContainer

logger = logging.getLogger(__name__)
blueprint = Blueprint('service_context', __name__)


@blueprint.route('/service-context', methods=['PATCH'])
@post_data_required
@inject
def update_service_context(
    json_data,
    service_context_service=Provide[
        DependencyContainer.service_context_service
    ]
):
    validated_data = ServiceContextSchema().load(json_data)
    service_context = service_context_service.update(validated_data)
    return create_response(service_context, ServiceContextSchema)


@blueprint.route('/service-context', methods=['GET'])
@inject
def get_service_status(
    service_context_service=Provide[
        DependencyContainer.service_context_service
    ]
):
    status = service_context_service.get_service_context()
    return create_response(status, ServiceContextSchema)
