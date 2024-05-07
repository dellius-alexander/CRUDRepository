"""
This module contains classes and functions for formatting log messages.
"""

from logging import Formatter, LogRecord
from typing import Literal, Optional, Any


class CustomFormatter(Formatter):
    """
    This class is used for custom formatting of log messages.
    """

    # Colors for log levels
    colors = {
        "DEBUG": "\033[1;36m",  # cyan
        "INFO": "\033[1;32m",  # green
        "WARNING": "\033[1;33m",  # yellow
        "ERROR": "\033[1;31m",  # red
        "CRITICAL": "\033[1;35m",  # magenta
    }

    def __init__(
        self,
        formatter: Optional[
            str
        ] = "[%(asctime)s] [%(levelname)s] [%(name)s][%(lineno)s]: %(message)s",
        datefmt: Optional[str] = "%Y-%m-%d %H:%M:%S",
        style: Literal["%"] = "%",
    ):
        # Overriding the 'format' method of the logging.Formatter class
        super().__init__(fmt=formatter, datefmt=datefmt, style=style, validate=True)

    def format(self, record: Any) -> str:
        """
        Format the specified record as text.

        :param record: The record to be formatted.
        :return: Formatted record as text.
        """
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        return s

    def formatMessage(self, record: Any) -> str:
        """
        Format the specified record's message as text.

        :param record: The record whose message is to be formatted.
        :return: Formatted message as text.
        """
        return (
            f"{record.asctime} - {record.name} - {record.levelname} - {record.message}"
        )

    def format_record(self, record: LogRecord):
        """Format the log record and return the formatted record
        :param record: the log record
        :return: the formatted log record
        """
        record.msg = self.format(record)
        return record
