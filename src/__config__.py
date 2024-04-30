#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module is used for managing the configuration of the CRUDRepository project.
"""
# --------------------------------------------------------------
import time
import os
import json
from dotenv import load_dotenv, find_dotenv, dotenv_values

# --------------------------------------------------------------
# Load environment variables from .env file
for filename in [".env"]:
    load_dotenv(
        find_dotenv(
            filename=filename,
            raise_error_if_not_found=True,
            usecwd=True,
        )
    )

# --------------------------------------------------------------
# Load environment variables
# This is your Project Root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # ~/.../CRUDRepository/src
# --------------------------------------------------------------
# This is your DATA Directory
DATA_DIR = os.path.join(ROOT_DIR, "data")  # ~/.../CRUDRepository/src/data
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_FILE = f'{ROOT_DIR}/logs/crud_{time.strftime("%Y%m%d%H%M%S")}.log'
LOG_DIR = os.path.join(ROOT_DIR, "logs")  # ~/.../CRUDRepository/src/logs
# --------------------------------------------------------------
# Set environment variables
os.environ.setdefault("ROOT_DIR", ROOT_DIR)
os.environ.setdefault("LOG_FILE", LOG_FILE)
os.environ.setdefault("LOG_LEVEL", LOG_LEVEL)
os.environ.setdefault("LOG_DIR", LOG_DIR)
print(json.dumps(dotenv_values(), indent=2, sort_keys=True))
# --------------------------------------------------------------
# Define log colors
log_colors_config = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red",
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
            "style": "%",
        },
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s[%(asctime)s][%(levelname)s][%(name)s][%(lineno)s]: "
            "\n%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": log_colors_config,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "colored",
        },
        "file_handler": {
            "class": "src.my_logger.handlers.CustomTimedRotatingFileHandler",
            "filename": f"{LOG_FILE}",
            "when": "midnight",
            "interval": 1,
            "backup_count": 2,  # Modified this line to keep only 2 log files
            "encoding": "utf-8",
            "delay": False,
            "utc": False,
            "level": "DEBUG",
            "formatter": "standard",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console", "file_handler"],
            "level": "DEBUG",
            "propagate": True,
        }
    },
}
# --------------------------------------------------------------
