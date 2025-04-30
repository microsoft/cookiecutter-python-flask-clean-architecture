from .base_model import BaseModel

class Todo(BaseModel):

    def __init__(
        self,
        title,
        description,
        created_at=None,
        updated_at=None,
        completed=False
    ):
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return self.repr(
            title=self.title,
            description=self.description,
            completed=self.completed,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
