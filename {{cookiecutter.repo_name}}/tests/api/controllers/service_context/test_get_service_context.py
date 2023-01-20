import json

from tests.resources import AppTestBase


class Test(AppTestBase):

    def setUp(self) -> None:
        super(Test, self).setUp()
        self.setup_database()

    def test_retrieve_status(self):
        response = self.client.get('/v1/service-context')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(False, data['maintenance'])
