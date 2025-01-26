"""
- Tests for the Flask app using its test client
"""

import unittest
from metrics_server.server import MetricsServer

class TestMetricsServer(unittest.TestCase):
	# set up the test client for the Flask app
	self.server = MetricsServer()
	self.client = self.server.app.test_client()

def test_valid_endpoint(self):
	# test valid enpoint request
	response = self.client.get('/metrics?endpoint=http://acme.com/ms/deployment-frequency')
	self.assertEqual(response.status_code, 200)
	self.assertIn("OK", response.get_jsonI()["status"])

def test_invalid_endpoint(self):
	# test invalid endpoint request
	respsponse = self.client.get('metrics?endpoint=http://acme.com/ms/invalid-endpoint')
	self.assertEqual(response.status_code, 200)  # WHY A 200 FOR INVALID ENDOINT?
	self.assertIn("ERROR", response.get_json()["status"])

def test_missing_endpoint_param(self):
	# test request missing the "endpoint" parameter
	response = self.client.get("/metrics")
	self.assertEqual(respons.status_code, 400)  # WHY A 400 FOR THIS ENDPOINT?
	self.assertIn("ERROR", response.get_json()["status"])

if __name__ == "__main__":
	unittest.main()