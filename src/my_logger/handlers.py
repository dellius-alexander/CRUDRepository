"""
This module contains custom logging handlers.
"""

import logging.handlers
import os
import traceback
import sys
import time
from logging import StreamHandler, DEBUG, Formatter
from typing import Optional

from src.my_logger.formatters import CustomFormatter


# ------------------------------------------------------------------------
class CustomStreamHandler(StreamHandler):
    """
    This class is a custom stream handler for logging.
    """

    def __init__(
        self,
        level: int = DEBUG,
        formatter: Optional[Formatter] = CustomFormatter(),
        stream=sys.stderr,
    ):
        try:
            super().__init__(stream=stream)
            super().setLevel(level)
            super().setFormatter(formatter)
        except IOError as e:
            print(f"IOError: {e}")
            traceback.print_exc()
        except ValueError as e:
            print(f"ValueError: {e}")
            traceback.print_exc()


# ------------------------------------------------------------------------
class CustomTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    This class is a custom timed rotating file handler for logging.
    """

    def __init__(self, **kwargs):
        """
        Initialize the CustomTimedRotatingFileHandler.

        All parameters are now taken from **kwargs.
        """

        # Extract arguments using kwargs.get()
        filename = kwargs.get(
            "filename",
            f'{os.getenv("ROOT_DIR")}/logs/log_{time.strftime("%Y%m%d%H%M%S")}.log',
        )
        when = kwargs.get("when", "h")
        interval = kwargs.get("interval", 1)
        backup_count = kwargs.get("backup_count", 5)
        encoding = kwargs.get("encoding", None)
        delay = kwargs.get("delay", False)
        utc = kwargs.get("utc", False)
        at_time = kwargs.get("at_time", None)
        level = kwargs.get("level", logging.WARN)
        formatter = kwargs.get("formatter", None)

        try:
            super().__init__(
                filename=filename,
                when=when,
                interval=interval,
                backupCount=backup_count,
                encoding=encoding,
                delay=delay,
                utc=utc,
                atTime=at_time,
            )
            super().setFormatter(formatter)
            self.setLevel(level)
            self.cleanup_old_logs()
        except IOError as e:
            print(f"IOError: {e}")
            traceback.print_exc()
        except ValueError as e:
            print(f"ValueError: {e}")
            traceback.print_exc()

    def getFilesToDelete(self):
        """
        Get the list of files to delete
        :return: list of files to delete
        """
        try:
            log_dir = os.getenv("LOG_DIR")
            # get the files in the log directory
            file_names = os.listdir(log_dir)
            # sort the array based on file creation time
            file_names.sort(key=lambda x: os.path.getmtime(os.path.join(log_dir, x)))
            # rebuild the file paths
            file_names = [
                os.path.join(str(log_dir), str(file_name)) for file_name in file_names
            ]

            # Calculate the number of files to delete based on the backup count
            num_files_to_delete = max(0, len(file_names) - self.backupCount)

            # Get the files to delete
            files_to_delete = file_names[:num_files_to_delete]

            #     print(f"""
            # Logging Dir: {log_dir}
            # Base file name: {base_file_name}
            # Backup count: {self.backup_count}
            # Log Files: {file_names}
            # Log Files Exceeded Limit: {num_files_to_delete}
            # Sorted Files: {file_names}
            # Files to delete: {files_to_delete}
            #                 """)
            return files_to_delete
        except Exception as e:
            print(f"Error getting files to delete: {e}")
            traceback.print_exc()
            return []

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit the log record
        :param record:
        :return:
        """
        logging.handlers.TimedRotatingFileHandler.emit(self, record)

    @classmethod
    def _delete_files(cls, files_to_delete):
        """
        Delete the files
        :param files_to_delete:
        :return:
        """
        # Delete files
        for file in files_to_delete:
            if os.path.exists(file):
                print(f"Deleting file: {file}")
                os.remove(file)
            else:
                print(f"File not found: {file}")

    def cleanup_old_logs(self):
        """Override the doRollover method to delete old log files."""
        # Now clean up old files
        files_to_delete = self.getFilesToDelete()
        self._delete_files(files_to_delete)

    def _limit(self, x):
        """
        Limit the number of log files to keep
        :param x:
        :return:
        """
        return max(0, len(x) - self.backupCount)


# ------------------------------------------------------------------------
