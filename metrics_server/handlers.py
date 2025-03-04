"""
- Encapsulates the business logic for fetching metrics
- Demonstrates how to use classes to manage data and logic
"""

import json

from metrics_server.logger import logger

# Load metric data from JSON file with error handling
try:
    with open("metrics_server/config/metric_data.json", "r") as f:
        METRIC_DATA = json.load(f)
    logger.info("Successfully loaded metric data.")
except Exception as e:
    logger.error("Failed to load metric data: %s", e)
    METRIC_DATA = {}

# Load the routes from the configuration file
try:
    with open("metrics_server/config/routes.json", "r") as f:
        ROUTES = json.load(f)
    logger.info("Successfully loaded routes configuration.")
except Exception as e:
    logger.error("Failed to load routes configuration: %s", e)
    ROUTES = {}

# Handler class for handling metric requests dynamically
class MetricHandler:
    def __init__(self, metric_name, server):
        """
        Initialize the handler with the metric name and the server instance.
        :param metric_name: Name of the metric being handled (e.g. 'deployment-frequency')
        :param server: Reference to the MetricsServer instance
        """
        self.metric_name = metric_name
        self.server = server

    def handle_request(self):
        """
        Handles the HTTP request for the metric.
        Logs the process using rich colored messages and returns the metric data.
        :return: dict with status and metric data/error message.
        """
        try:
            # Log the beginning of request handling
            logger.info(
                f"Processing request for metric: {self.metric_name}"
            )
            # Fetch data from the preloaded JSON fixture
            data = METRIC_DATA.get(self.metric_name)
            if data is None:
                # Log a warning if the metric is not found
                logger.error(f"Metric '{self.metric_name}' not found.")
                return {
                    "status": "Error",
                    "data": {"metric_name": self.metric_name, "value": "Metric not found"},
                }
            # Log success in retrieval
            logger.info(
                f"Successfully retrieved metric '{self.metric_name}' with value: {data}"
            )
            return {"status": "OK", "data": {"metric_name": self.metric_name, "value": data}}
        except Exception as e:
            # Log any unexpected errors during request handling
            logger.error("Error processing metric '%s': %s", self.metric_name, e)
            return {
                "status": "Error",
                "data": {"metric_name": self.metric_name, "value": "Internal error"},
            }

# Routes class for managing routes and their corresponding handlers
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