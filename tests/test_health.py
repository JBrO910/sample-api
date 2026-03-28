from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
import unittest


class HealthTest(unittest.TestCase):

    def setUp(self):
        settings.DISABLE_RATE_LIMIT = True
        self.client = TestClient(app)

    def test_health_full(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("db_connected", response.json())
        self.assertIn("has_data", response.json())

    def test_health_database_filter(self):
        response = self.client.get("/api/health?query=database")
        self.assertEqual(response.status_code, 200)
        self.assertIn("db_connected", response.json())

    def test_health_data_filter(self):
        response = self.client.get("/api/health?query=data")
        self.assertEqual(response.status_code, 200)
        self.assertIn("has_data", response.json())

    def test_invalid_query(self):
        response = self.client.get("/api/health?query=invalid")
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
