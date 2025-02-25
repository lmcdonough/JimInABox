import unittest
from main import app
from metrics_server.routes import Route

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.route_manager = Route()  # Instantiate Route class

    def test_get_metric_exists(self):
        # Use an existing metric from the JSON data
        existing_metric = list(self.route_manager.get_metric_data().keys())[0]
        response = self.client.get(f'/metrics/{existing_metric}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('metric', response.json['data'])

    def test_add_metric_valid(self):
        payload = '{"new_metric": 10}'
        response = self.client.post('/metrics', data=payload)
        self.assertIn('message', response.json['data'])