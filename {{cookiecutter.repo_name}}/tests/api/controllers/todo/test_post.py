import json

from tests.resources import AppTestBase


class Test(AppTestBase):

    def test_create_todo(self):
        todo_service = self.app.container.todo_service()
        self.assertEqual(
            0, len(todo_service.get_all({'itemized': True})["items"])
        )
        response = self.client.post(
            f'/v1/todo',
            data=json.dumps(
                {
                    "title": "test",
                    "description": "test"
                }
            ),
            content_type='application/json'
        )
        self.assertEqual(201, response.status_code)
        todo = todo_service.get(response.json['id'])
        self.assertEqual(todo.id, response.json['id'])
        self.assertEqual(todo.title, response.json['title'])
        self.assertEqual(todo.description, response.json['description'])
        self.assertEqual(False, response.json['completed'])
        todo = todo_service.get(todo.id)
        self.assertEqual(False, todo.completed)
