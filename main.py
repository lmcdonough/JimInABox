from datetime import datetime, timezone

from flask import Flask, request
from markupsafe import escape

from metrics_server.serializer import MetricsSerializer
from metrics_server.logger import logger
from metrics_server.server import MetricsServer
from metrics_server.routes import Route

# Initialize Flask app
app = Flask(__name__)

# Path to the metrics data file
METRICS_DATA_FILE = 'metrics_server/config/metric_data.json'

# Instantiate the Route class to load routes and metric data
route_manager = Route()

# Endpoint to dynamically fetch a specific metric
@app.route('/metrics/<metric_name>', methods=['GET'])
def get_metric(metric_name):
    try:
        metric_name = metric_name.strip()  # Remove leading/trailing whitespace
        logger.info(f'Fetching metric: {metric_name}')

        # Check if metric exists and return it
        metric_value = route_manager.get_metric_value(metric_name)
        if metric_value:
            logger.info(f'Metric {metric_name} found')

            # Serialize the metric data into a dictionary
            data = {
                "metric": escape(metric_name),
                "value": str(
                    escape(metric_value)
                ),  # ensure value is string safe for json
                "timestamp": datetime.now(timezone.utc).isoformat(
                    timespec='milliseconds'
                ),  # consistent iso timestamp format
            }
            return MetricsSerializer.serialize_response("OK", data)
        logger.warning(f'Metric {metric_name} not found')
        return MetricsSerializer.serialize_response("ERROR", {"error": "Metric not found"}), 404
    except Exception as e:
        logger.error(f'Unexpected error fetching metric {metric_name}: {str(e)}')
        return (
            MetricsSerializer.serialize_response("ERROR", {"error": "Internal server error"}),
            500,
        )

# Endpoint to add a new metric
@app.route('/metrics', methods=['POST'])
def add_metric():
    try:
        request_data = request.data  # Get raw request data
        logger.info("Received request to add metric")

        # Deserialize JSON data
        metric_data = MetricsSerializer.deserialize_request(request_data)
        if not metric_data:
            return MetricsSerializer.serialize_response("ERROR", {"error": "Invalid JSON"}), 400

        logger.info(f'Adding new metric: {metric_data}')

        # Update metrics data and write to file
        # Load existing metrics data
        existing_metrics = route_manager.get_metric_data()
        existing_metrics.update(metric_data)
        # Write updated metrics data to file
        MetricsSerializer.write_metrics_data(METRICS_DATA_FILE, existing_metrics)

        return MetricsSerializer.serialize_response("OK", {"message": "Metric added successfully"})
    except Exception as e:
        logger.error(f'Unexpected error adding metric: {e}')
        return (
            MetricsSerializer.serialize_response("ERROR", {"error": "Internal server error"}),
            500,
        )

if __name__ == "__main__":
    # create an run the metrics server
    # create an instance of the metrics server and pass in the Flask app instance
    server = MetricsServer(app=app)
    server.setup_routes()
    server.run()