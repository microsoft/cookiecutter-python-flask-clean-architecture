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
