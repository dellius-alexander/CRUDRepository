from logging import Formatter, LogRecord
from typing import Literal, Optional, Union


class CustomFormatter(Formatter):
    """Custom Logging Formatter"""

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
        format: Optional[
            str
        ] = "[%(asctime)s] [%(levelname)s] [%(name)s][%(lineno)s]: %(message)s",
        datefmt: Optional[str] = "%Y-%m-%d %H:%M:%S",
        style: Literal["%"] = "%",
    ):
        # Overriding the 'format' method of the logging.Formatter class
        super().__init__(fmt=format, datefmt=datefmt, style=style, validate=True)

    def format(self, record: LogRecord):
        """Format the log message
        :param record: the log record
        :return: the formatted log message
        """
        level_name = record.levelname
        msg = Formatter.format(self, record)
        return "%s%s\033[1;0m" % (self.colors[level_name], msg)

    def format_record(self, record: LogRecord):
        """Format the log record and return the formatted record
        :param record: the log record
        :return: the formatted log record
        """
        record.msg = self.format(record)
        return record
