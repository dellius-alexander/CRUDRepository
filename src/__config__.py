import dotenv
import time
import dotenv
import os

# --------------------------------------------------------------
# Load environment variables from .env file
for filename in [".env", ".env.postgres"]:
    dotenv.load_dotenv(dotenv.find_dotenv(
        filename=filename,
        raise_error_if_not_found=True,
        usecwd=True,
    ))
DEFAULT_SERVER_PORT = os.getenv("DEFAULT_SERVER_PORT", "8000")
# --------------------------------------------------------------
# Load environment variables
# This is your Project Root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # ~/.../neuralNetworks/src
# print(f"Root directory: {ROOT_DIR}")
# This is your DATA Directory
DATA_DIR = os.path.join(ROOT_DIR, "data")  # ~/.../neuralNetworks/src/data
# print(f"Data directory: {DATA_DIR}")
LOG_FILE = f"""{os.getenv('LOG_DIR')}/app.{time.strftime("%Y%m%d%H%M")}.log"""
# print(f"Log file: {LOG_FILE}")
# Set environment variables
os.environ.setdefault('LOG_FILE', LOG_FILE)
os.environ.setdefault('ROOT_DIR', ROOT_DIR)
# --------------------------------------------------------------
# Define log colors
log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}
# --------------------------------------------------------------
# Logging configuration
log_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "class": "logging.Formatter",
            "format": "[%(asctime)s][%(levelname)s][%(name)s][%(lineno)s]: \n%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "%"
        },
        "colored": {
            '()': 'colorlog.ColoredFormatter',
            'format': "%(log_color)s[%(asctime)s][%(levelname)s][%(name)s][%(lineno)s]: \n%(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S",
            'log_colors': log_colors_config
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "colored"
        },
        "file_handler": {
            "class": "myLogger.Handlers.CustomTimedRotatingFileHandler",
            "filename": f"{LOG_FILE}",
            "when": "midnight",
            "interval": 1,
            "backup_count": 2,  # Modified this line to keep only 2 log files
            "encoding": "utf-8",
            "delay": False,
            "utc": False,
            "level": "DEBUG",
            "formatter": "standard"
        },
    },
    "loggers": {
        "root": {
            "handlers": ["default", "file_handler"],
            "level": "DEBUG",
            "propagate": True,
        }
    },
}
# --------------------------------------------------------------
