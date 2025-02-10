from tests.resources import AppTestBase


class Test(AppTestBase):

    def test_delete(self):
        todo_service = self.app.container.todo_service()
        todo = todo_service.create({
            "title": "test",
            "description": "test"
        })
        self.assertEqual(
            1, len(todo_service.get_all({'itemized': True})["items"])
        )
        response = self.client.delete(f'/v1/todo/{todo.id}')
        self.assertEqual(204, response.status_code)
        self.assertEqual(
            0, len(todo_service.get_all({"itemized": True})["items"])
        )
