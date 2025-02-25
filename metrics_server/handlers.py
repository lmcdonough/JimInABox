import json

# Import the logger
from metrics_server.logger import logger

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
        Logs the process and returns the metric data.
        :return: dict with status and metric data/error message.
        """
        try:
            # Log the beginning of request handling
            logger.info(f"Processing request for metric: {self.metric_name}")
            # Fetch data from the preloaded JSON fixture
            data = self.server.route_manager.get_metric_value(self.metric_name)
            if data is None:
                # Log a warning if the metric is not found
                logger.warning(f"Metric '{self.metric_name}' not found.")
                return {
                    "status": "Error",
                    "data": {"metric_name": self.metric_name, "value": "Metric not found"},
                }
            # Log success in retrieval
            logger.info(f"Successfully retrieved metric '{self.metric_name}' with value: {data}")
            return {"status": "OK", "data": {"metric_name": self.metric_name, "value": data}}
        except Exception as e:
            # Log any unexpected errors during request handling
            logger.error(f"Error processing metric '{self.metric_name}': {e}")
            return {
                "status": "Error",
                "data": {"metric_name": self.metric_name, "value": "Internal error"},
            }
