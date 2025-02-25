import json
from datetime import datetime, timezone
from flask import request
from markupsafe import escape

from metrics_server.logger import logger
from metrics_server.serializer import MetricsSerializer

class Route:
    def __init__(self):
        # Initialize empty dictionaries for routes and metric data
        self.routes = {}
        self.metric_data = {}
        # Load data from JSON files on initialization
        self._load_data()
        # Store the path to metric data file for reuse
        self.metric_data_file = 'metrics_server/config/metric_data.json'

    def _load_data(self):
        """Load routes and metric data from JSON files."""
        try:
            # Load route mappings from configuration
            with open("metrics_server/config/routes.json", "r") as f:
                self.routes = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load routes configuration: {e}")

        try:
            # Load metric data values from configuration
            with open("metrics_server/config/metric_data.json", "r") as f:
                self.metric_data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load metric data: {e}")

    def handle_get_metric(self, metric_name):
        """
        Handle GET request for a specific metric.
        Args:
            metric_name (str): Name of the metric to retrieve
        Returns:
            tuple: (response, status_code)
        """
        try:
            # Clean the input metric name
            metric_name = metric_name.strip()
            logger.info(f'Fetching metric: {metric_name}')

            # Attempt to get the metric value
            metric_value = self.get_metric_value(metric_name)
            if metric_value:
                logger.info(f'Metric {metric_name} found')
                # Prepare response data with timestamp
                data = {
                    "metric": escape(metric_name),
                    "value": str(escape(metric_value)),
                    "timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds')
                }
                return MetricsSerializer.serialize_response("OK", data)
            
            # Handle metric not found
            logger.warning(f'Metric {metric_name} not found')
            return MetricsSerializer.serialize_response("ERROR", {"error": "Metric not found"}), 404
        except Exception as e:
            # Handle unexpected errors
            logger.error(f'Unexpected error fetching metric {metric_name}: {str(e)}')
            return MetricsSerializer.serialize_response("ERROR", {"error": "Internal server error"}), 500

    def handle_add_metric(self):
        """
        Handle POST request to add a new metric.
        Returns:
            tuple: (response, status_code)
        """
        try:
            # Get raw request data
            request_data = request.data
            logger.info("Received request to add metric")

            # Attempt to deserialize the JSON data
            metric_data = MetricsSerializer.deserialize_request(request_data)
            if not metric_data:
                return MetricsSerializer.serialize_response("ERROR", {"error": "Invalid JSON"}), 400

            logger.info(f'Adding new metric: {metric_data}')

            # Update the metrics data in memory and persist to file
            self.metric_data.update(metric_data)
            MetricsSerializer.write_metrics_data(self.metric_data_file, self.metric_data)

            return MetricsSerializer.serialize_response("OK", {"message": "Metric added successfully"})
        except Exception as e:
            # Handle unexpected errors
            logger.error(f'Unexpected error adding metric: {e}')
            return MetricsSerializer.serialize_response("ERROR", {"error": "Internal server error"}), 500

    def get_route(self, metric_name):
        """
        Get the route for a given metric name.
        :param metric_name: Name of the metric.
        :return: The route for the metric, or None if not found.
        """
        return self.routes.get(metric_name)

    def get_routes(self):
        """
        Get all routes in the config file.
        :return: A dictionary of all routes.
        """
        if not self.routes:
            self._load_data()
        return self.routes

    def get_metric_data(self):
        """
        Get all metric data.
        :return: A dictionary of all metric data.
        """
        # Load data if not already loaded
        if not self.metric_data:
            self._load_data()
        return self.metric_data

    def get_metric_value(self, metric_name):
        """
        Get the value for a given metric name.
        :param metric_name: Name of the metric.
        :return: The value of the metric, or None if not found.
        """
        return self.metric_data.get(metric_name)