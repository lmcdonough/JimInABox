"""
- Encapsulates the business logic for fetching metrics
- Demonstrates how to use classes to manage data and logic
"""

import json
import os
from rich.console import Console

# console instance for logging
console = Console()

# business logic for handling metrics
class MetricsHandler(self):
	def __init__(self):
		# load the mock data on initialization
		self.data = self.load_mock_data()

	@staticmethod
	def load_mock_data():
		# load JSON data from the metrics.json file
		data_file = os.path.join(os.path.dirname(__file__), 'data', 'metrics.json')
		with open(data_file, 'r') as file:
			# log when data is successfully loaded
			console.log(f"[blue]Loaded mock data from {data_file}[/blue]")
			return json.load(file)

	def get_metric(self, endpoint):
		# Fetch metric data for the given endpoint
		response = self.data.get(endpoint)
		if response:
			# log success
			console.log(f"[green]Metric found for endpoint: {endpoint}[/green]")
			return ({"status": "OK", "data": response})
		# Log failure if not data is found
		console.log(f"[red]Nod metric found for endopint: {endpoint}[/red]")
		return {"status": "ERROR", "message": "Endpoint not found"}
