import time
from functools import wraps
import logging

from rich.logging import RichHandler

# Configure logging with RichHandler for informative logs
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
# Initialize the logger for the server
logger = logging.getLogger("metrics_logger")

# Decorator to log the execution time of a function
def log_request(func):
    """
    A decorator to log details about server request handling functions,
    including endpoint, HTTP method, execution time, and result.
    """
    @wraps(func)  # Ensure the wrapped function retains its original metadata
    def wrapper(*args, **kwargs):
        """
        The wrapper function logs details before AND after the wrapped function is executed
        """
        # Extract additional context for server logging
        # Assumes the first arg is the request obj in the server context
        request = args[0] if args else None
        endpoint = request.endpoint if request.hasattr(request, 'endpoint') else "Unknown Endpoint"
        http_method = request.method if request and hasattr(request, 'method') else "Unknown Method"

        # Log request start
        logger.info(f"[LOG] Incoming request to endpoint `{endpoint}` using `{http_method}` method.")
        logger.info(f"    Request Arguments: {args}, Keyword Arguments: {kwargs}")

        # Record the start time
        start_time = time.time()

        # Call the actual function being wrapped (e.g. the request handler)
        result = func(*args, **kwargs)

        # Record the end time and calculate the duration
        end_time = time.time()
        duration = end_time - start_time

        # Log request completion
        logger.info(f"[LOG] request to `{endpoint}` completed")
        logger.info(f"    Response: {result}")
        logger.info(f"    Execution time: {duration:.4f} seconds")

        # Return the result of the wrapped function
        return result

    return wrapper