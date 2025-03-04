# Logging request decorator
import logging
import time
from functools import wraps

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

# Custom theme for Rich logging
custom_theme = Theme({
    "logging.level.success": "green on black",
    "logging.level.debug": "blue on black",
    "logging.level.info": "green on black",
    "logging.level.warning": "yellow",
    "logging.level.error": "bold white on red",
    "logging.level.critical": "bold magenta on black",
    "special": "bold white on blue"
})

# Initialize Rich console for colorul logging
console = Console(theme=custom_theme)

# Configure logging with the RichHandler for informative logs
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=True, show_time=True, show_path=True)],
)

logger = logging.getLogger("metrics_handler")


# Decorator to log request details
def log_request(func):
    """
    A decorator to log details about server request handling functions,
    including endpoint, HTTP mehtod, execution time, and result.
    """
    @wraps(func)  # Ensure the wrapped function retains its original metadata
    def wrapper(*args, **kwargs):
        """
        The wrapper function logs details before and after the wrapped function is executed, specifically tailored for server request handlers.
        """
        # Extract additional context for server logging
        # Assumes the first arg is the request obj in the server context
        request = args[0] if args else None
        endpoint = request.endpoint if request.hasattr(request, 'endpoint') else "Unknown Endpoint"
        http_method = request.method if request and hasattr(request, 'method') else "Unknown Method"

        # Log request start
        logger.info(f"Incoming request to endpoint `{endpoint}` using `{http_method}` method.")
        logger.info('Request Arguments: {}, Keyword Arguments: {}', args, kwargs)

        # Record the start time
        start_time = time.time()

        # Call the actual function being wrapped (e.g. the request handler)
        result = func(*args, **kwargs)

        # Record the end time and calculate the duration
        end_time = time.time()
        duration = end_time - start_time


        # Log request completion
        logger.info('Request to `{}` completed', endpoint)
        logger.info(f"Response: {result}")
        logger.info("Execution time: {duration:.4f} seconds")

        # Return the resule
        return result
    
    return wrapper
