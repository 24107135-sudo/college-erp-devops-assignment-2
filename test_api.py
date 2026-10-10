import unittest

from app import app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})

    def test_prediction_rejects_missing_fields(self):
        response = self.client.post("/predict", json={})
        self.assertEqual(response.status_code, 400)

    def test_prometheus_metrics_endpoint(self):
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"college_erp_predictions_total", response.data)
        self.assertIn(b"college_erp_prediction_seconds", response.data)


if __name__ == "__main__":
    unittest.main()
