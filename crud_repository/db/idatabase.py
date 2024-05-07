#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides classes for managing databases.
"""
from abc import ABC, abstractmethod
from sqlalchemy import Engine, Connection
from sqlalchemy.orm import scoped_session, sessionmaker
from crud_repository.my_logger.logger import CustomLogger


# ---------------------------------------------------------
class IDatabase(ABC):
    """
    This class defines the interface for all databases.

    Attributes:
        engine (Engine): The SQLAlchemy engine for the database.
        session (Session): The SQLAlchemy session for the database.
    """
    engine: Engine
    session: scoped_session

    def connect(self) -> Connection:
        """
        Connect to the PostgreSQL database.
        :return: (Connection) The SQLAlchemy connection for the PostgreSQL database.
        """
        return self.engine.connect()

    def get_scoped_session(self) -> scoped_session:
        """
        Get a session from the PostgreSQL database.  .
        :return: (scoped_session) The SQLAlchemy session for the PostgreSQL database.
        """
        _scoped_session = scoped_session(sessionmaker(bind=self.engine))
        return _scoped_session

    def __dict__(self):
        return {"engine": self.engine, "session": self.session}

    def __repr__(self):
        return f"DatabaseInterface(engine={self.engine!r}, session={self.session!r})"


# ---------------------------------------------------------
