from tests.resources import AppTestBase


class Test(AppTestBase):

    def test_get(self):
        todo_service = self.app.container.todo_service()
        todo = todo_service.create({
            "title": "test",
            "description": "test"
        })
        self.assertEqual(
            1, len(todo_service.get_all({"itemized": True})["items"])
        )
        response = self.client.get(f'/v1/todo/{todo.id}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(todo.id, response.json['id'])
        self.assertEqual(todo.title, response.json['title'])
        self.assertEqual(todo.description, response.json['description'])
        self.assertEqual(todo.completed, response.json['completed'])