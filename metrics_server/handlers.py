"""
- Encapsulates the business logic for fetching metrics
- Demonstrates how to use classes to manage data and logic
"""

import json

from rich.console import Console

console = Console()

# Load example data from JSON fixtures
with open("metrics_server/config/metric_data.json", "r") as f:
    METRIC_DATA = json.load(f)

# Load the routes from the config file
with open("metrics_server/config/routes.json", "r") as f:
    ROUTES = json.load(f)

# Handler class for handling metric requests dynamically
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
            "data": {"metric_name": self.metric_name, "value": data},
        }

# Routes class for  managing routes and their corresponding handlers
class Routes:
    def __init__(self):
        self.routes = {}
        # Load routes from the config file
        with open("config/routes.json", "r") as f:
            self.routes = json.load(f)

    def get_route(self, metric_name):
        """
        Get the route for a given metric name
        :param metric_name: Name of the metric
        :return: The route for the metric, or None if not found
        """
        return self.routes.get(metric_name)

    def get_routes(self):
        """Get all routes in the config file
        :return: A dictionary of all routes
        """
        return self.routes