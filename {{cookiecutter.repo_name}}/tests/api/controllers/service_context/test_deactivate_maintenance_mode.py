from tests.resources import AppTestBase


class Test(AppTestBase):

    def setUp(self) -> None:
        super(Test, self).setUp()
        self.setup_database()
        self.service_context_service = self.app.container\
            .service_context_service()

    def test_deactivate_maintenance(self):
        self.service_context_service.activate_maintenance_mode()
        service_context = self.service_context_service.get_status()
        self.assertTrue(service_context.maintenance)
        response = self.client.get('/v1/maintenance/deactivate')
        self.assertEqual(200, response.status_code)
        service_context = self.service_context_service.get_status()
        self.assertFalse(service_context.maintenance)
