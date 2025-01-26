"""
- The entry point to run the server
"""

from metrics_server.server import MetricsServer

if __name__ == "__main__":
	# create an run the metrics server
	server = MetricsServer()
	server.run()
