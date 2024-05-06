#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides classes for managing databases.
"""
from abc import ABC, abstractmethod
from sqlalchemy import Engine, Connection
from sqlalchemy.orm import scoped_session
from src.my_logger.logger import CustomLogger


# ---------------------------------------------------------
class IDatabase(ABC):
    """
    This class defines the interface for all databases.

    Attributes:
        engine (Engine): The SQLAlchemy engine for the database.
        session (Session): The SQLAlchemy session for the database.
    """

    @abstractmethod
    def connect(self) -> Connection:
        """
        Connect to the database.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def get_session(self) -> scoped_session:
        """
        Get a session from the database.

        Returns:
            Session: The SQLAlchemy session for the database.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def __dict__(self):
        return {"engine": self.engine, "session": self.session}

    def __repr__(self):
        return f"DatabaseInterface(engine={self.engine!r}, session={self.session!r})"


# ---------------------------------------------------------
