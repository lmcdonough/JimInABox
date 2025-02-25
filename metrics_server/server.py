# import configuration and handlers
from metrics_server.handlers import MetricHandler
from metrics_server.logger import log_request, logger


# metrics server class
class MetricsServer:
    def __init__(self, app, route_manager):
        # Initialize the MetricsServer with the passed in Flask app instance
        self.app = app
        self.route_manager = route_manager

    def setup_routes(self):
        # Dynamically map routes to their corresponding handlers
        # Routes and URIs are defined in the ROUTES dictionary
        routes = self.route_manager.get_routes()
        for metric, uri in routes.items():
            # create a handler instance for the metric
            handler = MetricHandler(metric, self)
            # Provide a unique endpoint name based on the metric
            endpoint_name = f"handle_{metric}_request"
            # Map the route to the handler's handle_request method, with logging
            # then supply the unique endpoint to avoid overwriting.
            self.app.add_url_rule(uri, endpoint_name, log_request(handler.handle_request), methods=["GET"])

    def get_metric_data(self, metric_name):
        """
        Fetch data for a given metric from the JSON fixtures.
        :param metric_name: Name of the metric to fetch data for.
        :return: The value of the metric if available, otherwise an error message.
        """
        data = self.route_manager.get_metric_value(metric_name)
        if data == "Metric not found":
            logger.error(f"Error: Metric '{metric_name}' not found in data.")
        return data

    def run(self, host="0.0.0.0", port=5005, debug=True):
        """
        Runs the Flask server with the default args that specify the host, port, and mode.
        """
        self.app.run(host=host, port=port, debug=debug)