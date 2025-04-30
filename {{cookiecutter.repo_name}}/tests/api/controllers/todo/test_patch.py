import json

from tests.resources import AppTestBase


class Test(AppTestBase):

    def test_update_todo(self):
        todo_service = self.app.container.todo_service()
        todo = todo_service.create({
            "title": "test",
            "description": "test"
        })
        self.assertEqual(
            1, len(todo_service.get_all({'itemized': True})["items"])
        )
        response = self.client.patch(
            f'/v1/todo/{todo.id}',
            data=json.dumps({"completed": True}),
            content_type='application/json'
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(todo.id, response.json['id'])
        self.assertEqual(todo.title, response.json['title'])
        self.assertEqual(todo.description, response.json['description'])
        self.assertEqual(True, response.json['completed'])
        todo = todo_service.get(todo.id)
        self.assertEqual(True, todo.completed)
