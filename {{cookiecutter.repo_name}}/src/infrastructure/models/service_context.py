from src.infrastructure.databases import sqlalchemy_db as db
from src.infrastructure.models.model_extension import ModelExtension


class ServiceContext(db.Model, ModelExtension):
    __tablename__ = 'service_context'
    id = db.Column(db.Integer, primary_key=True)
    maintenance = db.Column(db.Boolean, default=False)
