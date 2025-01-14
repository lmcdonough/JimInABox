from flask import Flask, abort, jsonify

# Base class for handling metrics
class BaseMetricsServer:
    def __init__(self):
        # Store endpoints and their corresponding metric retrieval functions
        self.metrics_map = {}

    def add_metric(self, endpoint, retrieval_function):
        """
        Register a new metric endpoint with a retrieval function.
        :param endpoint: API route for the metric (e.g., "/deployment-frequency")
        :param retrieval_function: Function to calculate or retrieve the metric
        """
        self.metrics_map[endpoint] = retrieval_function

    def get_metric(self, endpoint):
        """
        Retrieve metric data for a given endpoint.
        :param endpoint: API route
        :return: JSON response with status and data
        """
        if endpoint in self.metrics_map:
            return {"status": "OK", "data": self.metrics_map[endpoint]()}
        return {"status": "Error", "message": "Endpoint not found"}

# Child class for specific metrics
class MetricsServer(BaseMetricsServer):
    def __init__(self):
        super().__init__()

        # Registering specific metrics with their retrieval functions
        self.add_metric("/deployment-frequency", self.get_deployment_frequency)
        self.add_metric("/change-lead-time", self.get_change_lead_time)

    # Example metric retrieval functions
    @staticmethod
    def get_deployment_frequency():
        return {"deployment-frequency": 42}

    @staticmethod
    def get_change_lead_time():
        return {"change-lead-time": "15 minutes"}

# Flask application setup
app = Flask(__name__)

# Create an instance of the MetricsServer
metrics_server = MetricsServer()

@app.route("/<path:endpoint>", methods=["GET"])
def handle_request(endpoint):
    """
    Handle incoming GET requests and retrieve metrics using MetricsServer.
    :param endpoint: The API endpoint requested
    :return: JSON response with the metric data or an error message
    """
    response = metrics_server.get_metric(f"/{endpoint}")
    if response["status"] == "Error":
        abort(404, description=response["message"])
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)