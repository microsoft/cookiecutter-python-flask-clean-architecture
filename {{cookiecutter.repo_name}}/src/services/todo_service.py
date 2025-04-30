from datetime import datetime, timezone

from .repository_service import RepositoryService

class TodoService(RepositoryService):

    def create(self, data):
        data["created_at"] = datetime.now(tz=timezone.utc)
        return self.repository.create(data)

    def update(self, object_id, data):
        data["updated_at"] = datetime.now(tz=timezone.utc)
        return self.repository.update(object_id, data)
