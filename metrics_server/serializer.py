import json
import logging

from flask import jsonify

# Configure logging
logger = logging.getLogger(__name__)

# Class to serialize/deserialize metrics data
class MetricsSerializer:

    # Serialize response into JSON format
    @staticmethod
    def serialize_response(status, data):
        try:
            response = {"status": status, "data": data}
            return jsonify(response)
        except Exception as e:
            logger.error('Error serializing response: %s', e)
            return jsonify({"status": "ERROR", "data": {"error": "Internal server error"}}), 500

    # Deserialize request data from JSON format
    @staticmethod
    def deserialize_request(request_data):
        try:
            return json.loads(request_data)
        except json.JSONDecodeError as e:
            logger.error('Error deserializing request: %s', e)
            return None

    # Read metrics data from JSON file
    @staticmethod
    def read_metrics_data(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            logger.error('Error reading metrics data: %s', e)
            return {}

    # Write metrics data to JSON file
    @staticmethod
    def write_metrics_data(file_path, data):
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            logger.error('Error writing metrics data: %s', e)