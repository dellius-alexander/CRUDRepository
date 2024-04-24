"""
This module contains the CommandLogger class which is used for logging command events.
"""

from src.my_logger.logger import CustomLogger

log = CustomLogger(__name__).get_logger("DEBUG")


class CommandLogger:
    """
    This class is used for logging command events.
    """

    @classmethod
    def started(cls, event):
        """
        Logs the start of a command event.

        :param event: The event to be logged.
        :return: None
        """
        log.debug(
            "Command %s with request id %s started on server %s",
            event.command_name,
            event.request_id,
            event.connection_id,
        )

    @classmethod
    def succeeded(cls, event):
        """
        Logs the success of a command event.

        :param event: The event to be logged.
        :return: None
        """
        log.debug(
            "Command %s with request id %s on server %s succeeded in %s microseconds",
            event.command_name,
            event.request_id,
            event.connection_id,
            event.duration_micros,
        )

    @classmethod
    def failed(cls, event):
        """
        Logs the failure of a command event.

        :param event: The event to be logged.
        :return: None
        """
        log.debug(
            "Command %s with request id %s on server %s failed in %s microseconds",
            event.command_name,
            event.request_id,
            event.connection_id,
            event.duration_micros,
        )
