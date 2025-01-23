import logging
from logging.handlers import TimedRotatingFileHandler
import os

from app.config import Config

def configure_logging(app):
    """
    Configures logging for the Flask application.
    """
    
    if not os.path.exists(Config.LOG_DIRECTORY):
        os.makedirs(Config.LOG_DIRECTORY)
    
    # Create a custom logger
    logger = logging.getLogger("werkzeug")
    logger.setLevel(logging.DEBUG)  # Set global log level

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Console log level

    # Create a file handler (rotating log files)
    file_handler = TimedRotatingFileHandler(filename=os.path.join(Config.LOG_DIRECTORY, "app.log"), when='d')
    file_handler.setLevel(logging.INFO)  # File log level

    # Define the log format
    # log_format = logging.Formatter(
    #     "%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s"
    # )
    # console_handler.setFormatter(log_format)
    # file_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Attach logger to the Flask app
    # app.logger = logger
    # app.logger.propagate = False
    app.logger = logger
