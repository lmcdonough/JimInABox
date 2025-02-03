"""
- The entry point to run the server
"""
# import the metrics server class
from metrics_server.app import app

# import the Flask app instance
from metrics_server.server import MetricsServer

if __name__ == "__main__":
    # create an run the metrics server
    # create an instance of the metrics server and pass in the Flask app instance
    server = MetricsServer(app=app)
    server.run()