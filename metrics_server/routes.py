import json

# Import the logger
from metrics_server.logger import logger

class Route:
    def __init__(self):
        self.routes = {}
        self.metric_data = {}
        self.load_data()

    def load_data(self):
        """
        Load routes and metric data from JSON files.
        """
        try:
            with open("metrics_server/config/routes.json", "r") as f:
                loaded_routes = json.load(f)

            # Log routes if self.routes is empty (first load)
            if not self.routes:
                logger.info("Loaded routes config for metrics:\n%s", "\n".join(loaded_routes.keys()))
            self.routes = loaded_routes
        except Exception as e:
            logger.error(f"Failed to load routes configuration: {e}")
            self.routes = {}

        try:
            with open("metrics_server/config/metric_data.json", "r") as f:
                loaded_metric_data = json.load(f)

            # Log metric data if self.metric_data is empty (first load)
            if not self.metric_data:
                logger.info("Loaded metric data for metrics:\n%s", "\n".join(list(loaded_metric_data.keys())))
            self.metric_data = loaded_metric_data
        except Exception as e:
            logger.error(f"Failed to load metric data: {e}")
            self.metric_data = {}

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
        return self.routes

    def get_metric_data(self):
        """
        Get all metric data.
        :return: A dictionary of all metric data.
        """
        return self.metric_data

    def get_metric_value(self, metric_name):
        """
        Get the value for a given metric name.
        :param metric_name: Name of the metric.
        :return: The value of the metric, or None if not found.
        """
        return self.metric_data.get(metric_name)