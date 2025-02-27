# Logging request decorator
import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme


import time
from functools import wraps

# Import necessary modules
from flask import request

# Rich Logging Class
class RichLogger:
    """
    A custom logger class that uses Rich for colorful logging.
    """

    def __init__(self, name, level=logging.INFO, custom_theme=None):
        """
        Initialize the logger with the specified level and optional custom theme.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Define logging theme
            # Customize the theme
        custom_theme = Theme({
            "debug": "blue on black",
            "info": "green on black",
            "warning": "orange3",  # Added a new color
            "error": "bold white on red",
            "critical": "bold magenta on black",
            "special": "bold white on blue" # Added custom styling
        })
def log_request(func):
    """
    A decorator to log details about server request handling functions,
    including endpoint, HTTP mehtod, execution time, and result.
    """
    @wraps(func)  # Ensure the wrapped function retains its original metadata
    def wrapper(*args, **kwargs):
        """
        The wrapper function logs details before and after the wrapped function is executed
        Specifically tailored for server reques handlers.
        """
        # Extract additional context for server logging
        # Assumes the first arg is the request obj in the server context
        request = args[0] if args else None
        endpoint = request.endpoint if request.hasattr(request, 'endpoint') else "Unknown Endpoint"
        http_method = request.method if request and hasattr(request, 'method') else "Unknown Method"

        # Log request start
        print(f"[LOG] Incoming request to endpoint `{endpoint}` using `{http_method}` method.")
        print(f"    Rquest Arguments: {args}, Keyword Arguments: {kwargs}")

        # Record the start time
        start_time = time.time()

        # Call the actual function being wrapped (e.g. the request handler)
        result = func(*args, **kwargs)

        # Record the end time and calculate the duration
        end_time = time.time()
        duration = end_time - start_time

        # Log request completion
        print(f"[LOG] reuest to `{endpoint}` completed")
        print(f"    Response: {result}")
        print(f"    Execution time: {duration:.4f} seconds")

        # Return the result of the wrapped function
        return result

    return wrapper