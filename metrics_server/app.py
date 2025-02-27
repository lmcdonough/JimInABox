import logging
from datetime import datetime, timezone

from flask import Flask, request
from markupsafe import escape
from metrics_server.serializer import MetricsSerializer

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
    handlers=[RichHandler(rich_tracebacks=True, show_time=True, show_path=True)],
)

logger = logging.getLogger("metrics_handler")

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
        logger.info('Fetching metric: %s', metric_name)

        # Check if metric exists and return it
        if metric_name in metrics_data:
            logger.info('Metric %s found', metric_name)

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
        logger.info('Metric %s not found', metric_name)
        return MetricsSerializer.serialize_response("ERROR", {"error": "Metric not found"}), 404
    except Exception as e:
        logger.info('Unexpected error fetching metric %s: %s', metric_name, str(e))
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
        logger.info('Unexpected error adding metric: %s', e)
        return (
            MetricsSerializer.serialize_response("ERROR", {"error": "Internal server error"}),
            500,
        )

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run()