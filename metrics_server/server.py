# import configuration and handlers
from metrics_server.handlers import MetricHandler
from metrics_server.logger import log_request

from metrics_server.routes import Route
from rich.console import Console


# Initialize a consolse instance for rich logging
console = Console()

# metrics server class
class MetricsServer:
    def __init__(self, app):
        # Initialize the MetricsServier with the passed in Flask app instance
        self.app = app
        self.route_manager = Route()

    def setup_routes(self):
        # Dynamically map routes to their corresponding handlers
        # Routes and URIs are defined in the ROUTES dictionary
        routes = self.route_manager.get_routes()
        for metric, uri in routes.items():
            # create a handler instance for the metric
            handler = MetricHandler(metric, self)
            # Provide a unique endpoint name based on the metric
            endpoint_name = f"handle_{metric}_request"
            # Map the route to the handler's handle_request method, with logging,
            # and supply the unique endpoint to avoid overwriting.
            self.app.route(uri, methods=["GET"], endpoint=endpoint_name)(log_request(handler.handle_request))

    def get_metric_data(self, metric_name):
        """
        Fetch data for a given metric from the JSON fixtures.
        :param metric_name: Name of the metric to fetch data for.
        :return: The value of the metric if available, otherwise an error message.
        """
        console.log(f"Fetching data for metric: [blue]{metric_name}[/blue]")
        data = self.route_manager.get_metric_value(metric_name)
        if data == "Metric not found":
            console.log(f"[red]Error: Metric '{metric_name}' not found in data.[/red]")
        return data

    def run(self, host="0.0.0.0", port=5005, debug=True):
        """
        Runs the Flask server with the default args that specify the host, port, and mode.
        """
        console.log(f"[green]Starting MetricsServer on {host}:{port}[/green]")
        self.app.run(host=host, port=port, debug=debug)