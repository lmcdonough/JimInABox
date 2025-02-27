"""
- Defines the Flask app and routes
- Logs requests using a custom decorator
- Keeps routes minimal by delegating logic to handlers.py
"""
import logging

# import metrics config
from metrics_server.handlers import METRIC_DATA, MetricHandler, ROUTES

from metrics_server.logger import log_request

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme


# Define a custom theme for Rich logging
custom_theme = Theme({
    "logging.level.success": "green on black",
    "logging.level.debug": "blue on black",
    "logging.level.info": "green on black",
    "logging.level.warning": "yellow",  # Added a new color
    "logging.level.error": "bold white on red",
    "logging.level.critical": "bold magenta on black"
})

# Initialize Rich console for colorful logging
console = Console(theme=custom_theme)

# Configure the RichHandler with the console
handler = RichHandler(console=console, show_time=True, show_path=True)

# Configure logging with RichHandler for informative logs
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("metrics_handler")

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

    @staticmethod
    def get_metric_data(metric_name):
        """
        Fetch data for a given metric from the JSON fixtures
        :param metric_name: Name of the metric to fetch data for
        :return: The value of the metric if available, otherwise an error message
        """
        logger.info(f"Fetching data for metric: {metric_name}")
        data = METRIC_DATA.get(metric_name, "Metric not found")
        if data == "Metric not found":
            logger.info(f"Error: Metric '{metric_name}' not found in data.")
        return data

    # method to start the Flask server
    def run(self, host="0.0.0.0", port=5005, debug=True):
        """
        Runs the Flask server with the default args that specify the host, port, and mode.
        """
        # Log server startup details
        logger.info(f"Starting MetricsServer on {host}:{port}")
        # start the Flask app with the passed in args
        self.app.run(host=host, port=port, debug=debug)