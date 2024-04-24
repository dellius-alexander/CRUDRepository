"""
This module contains the CustomLogger class which is used for custom logging.
"""

import logging
import logging.config
import sys

from src.__config__ import log_config


# ---------------------------------------------------------
class CustomLogger(logging.Logger):
    """
    This class is used for custom logging.
    """

    def __init__(self, name, level=logging.INFO, config=None):
        """
        Initialize the logger with the given name and configuration.

        :param name: The name of the logger.
        :param level: The logging level.
        :param config: The configuration for the logger.
        """
        super().__init__(name, level)
        self.name = name
        if config is None:
            config = log_config
        try:
            logging.config.dictConfig(config)
        except ValueError as e:
            logging.error("Failed to configure logger: %s", e)
            sys.exit(1)

    def get_logger(self, level):
        """
        Get a logger instance with the specified level.

        :param level: The level of the logger.
        :return: A logger instance.
        """
        logger = logging.getLogger(self.name)
        logger.setLevel(level)
        return logger
