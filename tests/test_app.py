import unittest
from unittest.mock import patch

from metrics_server.app import app


class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_get_metric_exists(self):
        response = self.client.get('/metrics/existing_point')
        self.assertEqual(response.status_code, 200)
        self.assertIn('metric', response.json['data'])

    def test_add_metric_valid(self):
        payload = '{"new_metric": 10}'
        response = self.client.post('/metrics', data=payload)
        self.assertIn('message', response.json['data'])

# test class using mock and patch
class MetricEndpointTest(unittest.TestCase):
    def setUp(self):
        # Create a test client for the Flask app
        self.app = app.test_client()

    # patch the get_metric_data method to return a mock metric
    @staticmethod
    @patch('metrics_server.handlers.MetricsServer.get_metric_data')
    def test_get_metric(mock_get_metric_data):
        mock_get_metric_data.return_value = "Mocked Metric Data"
  #TODO add mock data from json fixture