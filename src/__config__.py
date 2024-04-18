#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module is used for managing the configuration of the CRUDRepository project.
"""
# --------------------------------------------------------------
import time
import os
import dotenv


# --------------------------------------------------------------
# Load environment variables from .env file
for filename in [".env"]:
    dotenv.load_dotenv(
        dotenv.find_dotenv(
            filename=filename,
            raise_error_if_not_found=True,
            usecwd=True,
        )
    )
# --------------------------------------------------------------
# Load environment variables
# This is your Project Root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # ~/.../neuralNetworks/src
# --------------------------------------------------------------
# This is your DATA Directory
DATA_DIR = os.path.join(ROOT_DIR, "data")  # ~/.../neuralNetworks/src/data
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_FILE = os.getenv("LOG_FILE", f'{ROOT_DIR}/logs/log_{time.strftime("%Y%m%d_%H%M%S")}.log')
# --------------------------------------------------------------
# Set environment variables
os.environ.setdefault("ROOT_DIR", ROOT_DIR)
os.environ.setdefault("LOG_FILE", LOG_FILE)
os.environ.setdefault("LOG_LEVEL", LOG_LEVEL)
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
            "class": "my_logger.handlers.CustomTimedRotatingFileHandler",
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
