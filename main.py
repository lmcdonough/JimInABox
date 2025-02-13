import argparse
from datetime import datetime, timezone

from flask import Flask
from rich.console import Console
from rich.table import Table

from metrics_server.logger import logger
from metrics_server.server import MetricsServer
from metrics_server.routes import Route

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run the Metrics Server.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host for the server.")
    parser.add_argument("--port", type=int, default=5005, help="Port for the server.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()

    # Initialize Flask app
    app = Flask(__name__)
    # Instantiate the Route class to load routes and metric data
    route_manager = Route()

    # Create and configure the metrics server
    server = MetricsServer(app=app, route_manager=route_manager)
    server.setup_routes()

    # Initialize Rich console for formatted output
    console = Console()
    
    # Create table to display available endpoints
    table = Table(title="Loaded Metrics and Endpoints", show_lines=True)
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("URL", style="magenta")

    # Add each route to the table
    routes = route_manager.get_routes()
    for metric, url in routes.items():
        fqdn = f"http://{args.host}:{args.port}{url}"
        table.add_row(metric, fqdn)

    # print new line for spacing
    console.print()

    # Display server information and endpoints table 
    console.print(table)

    # print new line for spacing
    console.print()
    
    # Start the server
    server.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()