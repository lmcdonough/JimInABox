"""
- Tests for the Flask app using its test client
- Run the using poetry run test or manually using python -m unittest tests.test_server.py
"""

import unittest
import json
from main import app  # Import the Flask app instance

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a test client
        cls.client = app.test_client()
        # load the endpoints to make GET requests to and load them into a class dictionary for the methods to refer to and use the requests library and start the actual dev sever
        cls.route_manager = TestApp.client.get('/routes').json()
        # load the metrics to make GET requests to and load them into a class dictionary for the methods to refer to and use the requests library and start the actual dev sever
        cls.metric_manager = TestApp.client.get('/metrics').json()

    def test_get_metric_exists(self):
        # Get an existing metric from the JSON data
        existing_metric = list(TestApp.route_manager.get_metric_data().keys())[0]
        response = self.client.get(f'/metrics/{existing_metric}')

        # Assert that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the metric
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('metric', data['data'])

    def test_get_metric_not_exists(self):
        # Get a non-existing metric
        response = self.client.get('/metrics/non_existing_metric')

        # Assert that the status code is 404
        self.assertEqual(response.status_code, 404)

    def test_add_metric_valid(self):
        # Add a new metric
        payload = json.dumps({"new_metric": 10})
        response = self.client.post('/metrics', data=payload, content_type='application/json')

        # Assert that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the message
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('message', data['data'])

if __name__ == '__main__':
    unittest.main()