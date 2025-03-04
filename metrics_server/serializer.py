import json

from flask import jsonify
from metrics_server.logger import logger

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
            logger.error("Error serializing response: %s", e)
            return jsonify({"status": "ERROR", "data": {"error": "Internal server error"}}), 500

    # Deserialize request data from JSON format, logging with rich coloring
    @staticmethod
    def deserialize_request(request_data):
        try:
            return json.loads(request_data)
        except json.JSONDecodeError as e:
            logger.error("Error deserializing request: %s", e)
            return None

    # Read metrics data from JSON file with rich logging on error
    @staticmethod
    def read_metrics_data(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                logger.info("Successfully loaded metrics data from %s", file_path)
                return data
        except Exception as e:
            logger.error("Error reading metrics data from %s: %s", file_path, e)
            return {}

    # Write metrics data to JSON file with informative rich logs
    @staticmethod
    def write_metrics_data(file_path, data):
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            logger.info("Metrics data successfully written to %s", file_path)
        except Exception as e:
            logger.error("[Error writing metrics data to %s: %s", file_path, e)