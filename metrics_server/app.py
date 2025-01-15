import logging
from datetime import datetime

from flask import Flask, request
from markupsafe import escape
from metrics_server.serializer import MetricsSerializer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Path to the metrics data file
METRICS_DATA_FILE = 'metrics_server/data/metrics_data.json'

# Load metrics data from a separate JSON file
metrics_data = MetricsSerializer.read_metrics_data(METRICS_DATA_FILE)

# Endpoint to dynamically fetch a specific metric
@app.route('/metrics/<metric_name>', methods=['GET'])
def get_metric(metric_name):
    try:
        metric_name = metric_name.strip()  # Remove leading/trailing whitespace
        logger.info('Fetching metric: %s', metric_name)

        # Check if metric exists and return it
        if metric_name in metrics_data:
            data = {
                "metric": escape(metric_name),
                "value": escape(metrics_data[metric_name]),
                "timestamp": datetime.now(datetime.timezone.utc).isoformat(),
            }
            return MetricsSerializer.serialize_response("OK", data)
        logger.warning('Metric %s not found', metric_name)
        return MetricsSerializer.serialize_response("ERROR", {"error": "Metric not found"}), 404
    except Exception as e:
        logger.error('Unexpected error fetching metric %s: %s', metric_name, str(e))
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

        logger.info('Adding new metric: %s', metric_data)

        # Update metrics data and write to file
        metrics_data.update(metric_data)
        MetricsSerializer.write_metrics_data(METRICS_DATA_FILE, metrics_data)

        return MetricsSerializer.serialize_response("OK", {"message": "Metric added successfully"})
    except Exception as e:
        logger.error('Unexpected error adding metric: %s', e)
        return (
            MetricsSerializer.serialize_response("ERROR", {"error": "Internal server error"}),
            500,
        )

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)