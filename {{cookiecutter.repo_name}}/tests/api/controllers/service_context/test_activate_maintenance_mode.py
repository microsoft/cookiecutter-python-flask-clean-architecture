from tests.resources import AppTestBase


class Test(AppTestBase):

    def setUp(self) -> None:
        super(Test, self).setUp()
        self.setup_database()
        self.service_context_service = self.app.container\
            .service_context_service()

    def test_activate_maintenance(self):
        service_context = self.service_context_service.get_status()
        self.assertFalse(service_context.maintenance)
        response = self.client.get('/v1/maintenance/activate')
        self.assertEqual(200, response.status_code)
        service_context = self.service_context_service.get_status()
        self.assertTrue(service_context.maintenance)
