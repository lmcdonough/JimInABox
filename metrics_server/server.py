"""
- Defines the Flask app and routes
- Logs requests using a custom decorator
- Keeps routes minimal by delegating logic to handlers.py
"""

import time
from functools import wraps
from flask import Flask, jsonify, request
from metrics_server.handlers import MetricsHandler
from rich.console import Console

# Initialize a consolse instance for rich logging
console = Console()


# Logging request decorator
def log_request(func):
	"""
	A decorator to log details about server request handling functions,
	including endpoint, HTTP mehtod, execution time, and result.
	"""
	@wraps(func)  # Ensure the wrapped function retains its original metadata
	def wrapper(*ars, **kwargs):
		"""
		The wrapper function logs details before and after the wrapped function is executed
		Specifically tailored for server reques handlers.
		"""
		# Extract additional context for server logging
		# Assumes the first arg is the request obj in the server context
		request = args[0] if args else None
		endpoint = request.endpoint if request.hasattr(request, 'endpoint') else "Unknown Endpoint"
		http_method = request.method if request and hasattr(request, 'method') else "Unknown Method"

		# Log request start
		print(f"[LOG] Incoming request to endpoint `{endpoint}` using `{http_method}` method.")
		print(f"	Rquest Arguments: {args}, Keyword Arguments: {kwargs}")

		# Record the start time
		start_time = time.time()

		# Call the actual function being wrapped (e.g. the request handler)
		result = func(*args, **kwargs)

		# Record the end time and calculate the duration
		end_time = time.time()
		duration = end_time - start_time

		# Log request completion
		print(f"[LOG] reuest to `{endpoint}` completed")
		print(f"	Response: {result}")
		print(f"	Execution time: {duration:.4f} seconds")

		# Return the result of the wrapped function
		return result

	return wrapper


# Flask server setup using a class based structure
class MetricsServer:
	def __init__(self):
		# Create the Flask app
		self.app = Flask(__name__)
		# Initialize the metrics handler (contains the business logic)
		self.handler = MetricsHandler()
		# Setup the routes for the app
		self.setup_routes()

	# sets up all routes and maps them to their handlers
	def setup_routes(self):
		"""
		Define all routes for the server, keeping routes minimal by delegating the logic to handlers
		"""
		@self.app.route('/metrics', methods=['GET'])  # Define a GET route for metrics
		@log_request  # Apply cool custom logging decorator we made
		def metrics():
			"""
			Handles incoming GET requests to the '/metrics' endpoint.
			Delegates the metric fetching to the MetricsHandler Class.
			"""
			# Get the "endpoint" parameter from the query string
			endpoint = request.args.get('endpoint')
			if not endpoint:
				# If the endpoint param is missing, return an error with an HTTP status code 400
				return jsonify({"status": "ERROR", "message": "Missing endpoint"}), 400

			# Use the handler to fetch the requested metric
			response = self.handler.get_metric(endpoint)

			# Return the response as JSON
			return jsonify(response)

	# method to start the Flask server
	def run(self, host="0.0.0.0", port=5000, debug=True):
		"""
		Runs the Flask server with the default args that specify the host, port, and mode.
		"""
		# Log server startup details
		console.log(f"[green]Starting MetricsServer on {host}:{port}[/green]")
		# start the Flask app with the passed in args
		self.app.run(host=host, port=port, debug=debug)














