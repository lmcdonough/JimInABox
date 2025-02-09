import json

from flask import jsonify
from metrics_server.logger import logger  # Import the logger


class MetricsSerializer:
    # Serialize response into JSON format, using rich logging for errors
    @staticmethod
    def serialize_response(status, data):
        try:
            # convert datetime objects to iso format before serialization

            response = {"status": status, "data": data}

            # return jsonified response
            return jsonify(response)
        except Exception as e:
            # log error and return 500 because serialization failed
            logger.error(f"[red]Error serializing response:[/red] {e}")
            return jsonify({"status": "ERROR", "data": {"error": "Internal server error"}}), 500

    # Deserialize request data from JSON format, logging with rich coloring
    @staticmethod
    def deserialize_request(request_data):
        try:
            return json.loads(request_data)
        except json.JSONDecodeError as e:
            logger.error(f"[red]Error deserializing request:[/red] {e}")
            return None

    # Read metrics data from JSON file with rich logging on error
    @staticmethod
    def read_metrics_data(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                logger.info(f"[green]Successfully loaded metrics data from {file_path}[/green]")
                return data
        except Exception as e:
            logger.error(f"[red]Error reading metrics data from {file_path}:[/red] {e}")
            return {}

    # Write metrics data to JSON file with informative rich logs
    @staticmethod
    def write_metrics_data(file_path, data):
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            logger.info(f"[green]Metrics data successfully written to {file_path}[/green]")
        except Exception as e:
            logger.error(f"[red]Error writing metrics data to {file_path}:[/red] {e}")