import json

# Import the logger
from metrics_server.logger import logger
from metrics_server.routes import Route

# Instantiate the Route class to load routes and metric data
route_manager = Route()

# Load metric data from JSON file with error handling
try:
    with open("metrics_server/config/metric_data.json", "r") as f:
        METRIC_DATA = json.load(f)
    logger.info("[green]Successfully loaded metric data.[/green]")
except Exception as e:
    logger.error(f"[red]Failed to load metric data:[/red] {e}")
    METRIC_DATA = {}

# Load the routes from the configuration file
try:
    with open("metrics_server/config/routes.json", "r") as f:
        ROUTES = json.load(f)
    logger.info("[green]Successfully loaded routes configuration.[/green]")
except Exception as e:
    logger.error(f"[red]Failed to load routes configuration:[/red] {e}")
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
                f"[bold blue]Processing request for metric:[/bold blue] [bold green]{self.metric_name}[/bold green]"
            )
            # Fetch data from the preloaded JSON fixture
            data = route_manager.get_metric_value(self.metric_name)
            if data is None:
                # Log a warning if the metric is not found
                logger.warning(f"[yellow]Metric '{self.metric_name}' not found.[/yellow]")
                return {
                    "status": "Error",
                    "data": {"metric_name": self.metric_name, "value": "Metric not found"},
                }
            # Log success in retrieval
            logger.info(
                f"[green]Successfully retrieved metric '{self.metric_name}' with value: {data}[/green]"
            )
            return {"status": "OK", "data": {"metric_name": self.metric_name, "value": data}}
        except Exception as e:
            # Log any unexpected errors during request handling
            logger.error(f"[red]Error processing metric '{self.metric_name}':[/red] {e}")
            return {
                "status": "Error",
                "data": {"metric_name": self.metric_name, "value": "Internal error"},
            }
