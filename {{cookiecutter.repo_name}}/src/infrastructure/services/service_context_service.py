from src.infrastructure.models import ServiceContext
from src.infrastructure.databases import sqlalchemy_db as db


class ServiceContextService:

    def update(self, data):
        service_context = ServiceContext.query.first()

        if service_context is None:
            service_context = ServiceContext()
            service_context.save(db)

        service_context.update(db, data)
        return service_context

    def get_service_context(self):
        status = ServiceContext.query.first()

        if status is None:
            status = ServiceContext()
            status.save(db)

        return status
