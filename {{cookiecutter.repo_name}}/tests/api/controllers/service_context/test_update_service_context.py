import json

from tests.resources import AppTestBase


class Test(AppTestBase):

    def setUp(self) -> None:
        super(Test, self).setUp()
        self.setup_database()
        self.service_context_service = self.app.container\
            .service_context_service()

    def test_update_service_context(self):
        service_context = self.service_context_service.get_service_context()
        self.assertFalse(service_context.maintenance)
        response = self.client.patch(
            '/v1/service-context',
            data=json.dumps({"maintenance": True}),
            content_type='application/json'
        )
        self.assertEqual(200, response.status_code)
        service_context = self.service_context_service.get_service_context()
        self.assertTrue(service_context.maintenance)
