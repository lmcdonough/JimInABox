import unittest
from flask import Flask
from app import app

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
