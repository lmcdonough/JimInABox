"""
- Encapsulates the business logic for fetching metrics
- Demonstrates how to use classes to manage data and logic
"""

import json
from rich.console import Console

console = Console()

# Load example data from JSON fixtures
with open("data/metrics_data.json", "r") as f:
	METRIC_DATA = json.load(f)

class MetricHandler:

	def __init__(self, metric_name, server):
		"""
		Initialize the handler withe the metric name and the server instance
		:param metric_name: Name of the metric being handled (e.g. 'deployment-frequency')
		:param server: Reference to the MetricsServer instance
		"""
		self.metric_name = metric_name
		self.server = server

	def handle_request(self):
		"""
		Handles the HTTP requests for the Metric.
		Fetches the data for the Metric and returns it in the expected format.
		:return: JSON response with the metric data
		"""

		# log to the console
		console.log(f"Processing request for metric: [bold green]{self.metric_name}[/bold green]")
		# Fetch data from the preloaded JSON fixture
		data = METRIC_DATA.get(self.metric_name, "Metric not found")
		# return the data or error message
		return {
			"status": "OK" if data != "Metri not found" else "Error",
			"data": {
				"metric_name": self.metric_name,
				"value": data
			}
		}
