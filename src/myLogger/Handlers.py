import logging.handlers
import os
import sys
from typing import Optional
from logging import LogRecord, StreamHandler, DEBUG, Formatter, FileHandler
from src.myLogger.Formatters import CustomFormatter

# ------------------------------------------------------------------------
class CustomStreamHandler(StreamHandler):
    def __init__(self, level: int = DEBUG, formatter: Optional[Formatter] = CustomFormatter(), stream=sys.stderr):
        try:
            super().__init__(stream=stream)
            super().setLevel(level)
            super().setFormatter(formatter)
        except Exception as e:
            print(f"Error: {e}")


# ------------------------------------------------------------------------
class CustomTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(
            self,
            filename,
            when='h',
            interval=1,
            backup_count=5,
            encoding=None,
            delay=False,
            utc=False,
            at_time=None,
            level=logging.WARN,
            formatter=None
    ):
        try:
            super().__init__(
                filename=filename,
                when=when,
                interval=interval,
                backupCount=backup_count,  # Pass backup_count to super
                encoding=encoding,
                delay=delay,
                utc=utc,
                atTime=at_time
            )
            super().setFormatter(formatter)
            self.setLevel(level)
            print(f"Log file: {os.getenv('LOG_FILE')}")
            print(f"Log dir: {os.getenv('LOG_DIR')}")
            print(f"Log level: {level}")
            self.cleanup_old_logs()
        except Exception as e:
            print(f"Error: {e}")

    def getFilesToDelete(self):
        """Get the list of files to delete
        :return: list of files to delete
        """
        log_dir = os.getenv("LOG_DIR")
        # get the files in the log directory
        file_names = os.listdir(log_dir)
        # sort the array based on file creation time
        file_names.sort(key=lambda x: os.path.getmtime(os.path.join(log_dir, x)))
        # rebuild the file paths
        file_names = [os.path.join(str(log_dir), str(file_name)) for file_name in file_names]

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

    def emit(self, record: logging.LogRecord) -> None:
        super().emit(record)

    def _delete_files(self, files_to_delete):
        # Delete files
        for file in files_to_delete:
            if os.path.exists(file):
                print(f"Deleting file: {file}")
                os.remove(file)
            else:
                print(f"File not found: {file}")

    def cleanup_old_logs(self):
        """ Override the doRollover method to delete old log files.
        """
        # Now clean up old files
        files_to_delete = self.getFilesToDelete()
        self._delete_files(files_to_delete)

    def _limit(self, x):
        return max(0, len(x) - self.backupCount)


# ------------------------------------------------------------------------
