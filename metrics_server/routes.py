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
                self.routes = json.load(f)
            logger.info("[green]Successfully loaded routes configuration.[/green]")
        except Exception as e:
            logger.error(f"[red]Failed to load routes configuration:[/red] {e}")
            self.routes = {}

        try:
            with open("metrics_server/config/metric_data.json", "r") as f:
                self.metric_data = json.load(f)
            logger.info("[green]Successfully loaded metric data.[/green]")
        except Exception as e:
            logger.error(f"[red]Failed to load metric data:[/red] {e}")
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