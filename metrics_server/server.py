"""
- Defines the Flask app and routes
- Logs requests using a custom decorator
- Keeps routes minimal by delegating logic to handlers.py
"""

import time
from functools import wraps

from flask import Flask, jsonify, request
from rich.console import Console  # import for sweet ass logging

from metrics_server.routes import ROUTES  # import routes config
from metrics_server.handlers import MetricHandler  # import handler class for processing requests
from metrics_server.logger import log_request  # handy dandy decorator I made for logging requests

# Initialize a consolse instance for rich logging
console = Console()

# metrics server class
class MetricsServer:
	def __init__(self, app):
		# Initialize the MetricsServier with the passed in Flask app instance
		self.app = app

	def setup_routes(self):
		# Dynamically map routes to their corresponding handlers
		# Routes and URIs are defined in the ROUTES dictionary
		for metric, uri in ROUTES.items():
			# create a handler instance for the metric
			handler = MetricHandler(metric, self)
			# Map the route to the handler's handle_request method, with logging
			self.app.route(uri, methods=["GET"])(log_request(handler.handle_request))

	def get_metric_data(self, metric_name):
		"""
		Fetch data for a given metric from the JSON fixtures
		:param metric_name: Name of the metric to fetch data for
		:return: The value of the metric if available, otherwise an error message
		"""
		console.log(f"Fetching data for metric: [bold blue]{metric_name}[/bold blue]")
		# Fetch data from the JSON fixture loaded in handlers.py
		data = METRIC_DATA.get(metric_name, "Metric not found")
		if data == "Metric not found":
			console.log(f"[bold red]Error:[/bold red] Metric '{metric_name}' not found in data.")
		return data

	# method to start the Flask server
	def run(self, host="0.0.0.0", port=5000, debug=True):
		"""
		Runs the Flask server with the default args that specify the host, port, and mode.
		"""
		# Log server startup details
		console.log(f"[green]Starting MetricsServer on {host}:{port}[/green]")
		# start the Flask app with the passed in args
		self.app.run(host=host, port=port, debug=debug)














