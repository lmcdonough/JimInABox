"""
- The entry point to run the server
"""
# import the metrics server class
from metrics_server.app import app

# import the Flask app instance
from metrics_server.server import MetricsServer

# wraps the server startup code
def main():
    # create an instance of the metrics server and run it
    server = MetricsServer(app=app)
    server.run()

if __name__ == "__main__":
    # run the server on the main thread
    main()