"""
- Defines the Flask app and routes
- Logs requests using a custom decorator
- Keeps routes minimal by delegating logic to handlers.py
"""

from flask import Flask, jsonify, request
from metrics_server.handlers import MetricsHandler
from rich.console import Console

# Initialize a consolse instance for rich logging
console = Console()

# a decorator to log API requests
def log_request(func):
	def wrapper(*args, **kwargs):  # REVIEW CREATING DECORATORS WITH A WRAPPER FUNCTION
		# Log the incoming request path and arguments
		console.log(f"[cyan]Incoming requesto to {request.path} with args {request.args}[/cyan]")
		return func(*args, **kwargs)
	return wrapper

# Class based Flask server setup
class MetricsServer:
	def __init__(self):
		# create the flask app
		self.app = Flask(__name__)
		# initialize the metrics handler (business logic)
		self.handler = MetricsHandler()
		# setup routes
		self.setup_routes()

	def setup_routes(self):
		# define a single route for fetching metrics
		@self.app.route('/metrics', method=['GET'])
		@log_request  # apply the logging decorator
		def metrics():
			# get the "endpoint" parameter from the request
			endpoint = request.args.get('endpoint')
			if not endpoint:
				# return an error and the http response code if the endpoint is missing
				return jsonify({"status": "ERROR", "message": "Missing endpoint"}), 400
			# delegate metric fetching to the handler
			response = self.handler.get_metric(endpoint)
			return jsonify(response)

	def run(self, host="0.0.0.0", port=5000, debug=True):
		# log server startup
		console.log(f"[green]Starting MetricsServer on {host}:{port}[/green]")
		self.app.run(host=host, port=port, debug=debug)
