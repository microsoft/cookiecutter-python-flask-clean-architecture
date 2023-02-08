from tests.resources import AppTestBase


class Test(AppTestBase):

    def setUp(self) -> None:
        super(Test, self).setUp()
        self.setup_database()
        self.service_context_service = self.app.container\
            .service_context_service()

    def test_get_service_context(self):
        service_context = self.service_context_service.get_service_context()
        self.assertFalse(service_context.maintenance)

    def test_update(self):
        service_context = self.service_context_service\
            .update({"maintenance": True})
        self.assertTrue(service_context.maintenance)
