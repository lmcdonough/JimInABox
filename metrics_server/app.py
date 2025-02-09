import logging
from datetime import datetime, timezone

from flask import Flask, request
from markupsafe import escape
from metrics_server.serializer import MetricsSerializer
from metrics_server.logger import logger  # Import the logger

# Initialize Flask app
app = Flask(__name__)

# Path to the metrics data file
METRICS_DATA_FILE = 'metrics_server/config/metric_data.json'

# Load metrics data from a separate JSON file
metrics_data = MetricsSerializer.read_metrics_data(METRICS_DATA_FILE)

# Endpoint to dynamically fetch a specific metric
@app.route('/metrics/<metric_name>', methods=['GET'])
def get_metric(metric_name):
    try:
        metric_name = metric_name.strip()  # Remove leading/trailing whitespace
        logger.info(f'Fetching metric: {metric_name}')

        # Check if metric exists and return it
        if metric_name in metrics_data:
            logger.info(f'Metric {metric_name} found')

            # Serialize the metric data into a dictionary
            data = {
                "metric": escape(metric_name),
                "value": str(
                    escape(metrics_data[metric_name])
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
        metrics_data.update(metric_data)
        MetricsSerializer.write_metrics_data(METRICS_DATA_FILE, metrics_data)

        return MetricsSerializer.serialize_response("OK", {"message": "Metric added successfully"})
    except Exception as e:
        logger.error(f'Unexpected error adding metric: {e}')
        return (
            MetricsSerializer.serialize_response("ERROR", {"error": "Internal server error"}),
            500,
        )

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run()