#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides classes for managing databases.
"""
from sqlalchemy import create_engine, Connection, text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database

from src.db.database_interface import DatabaseInterface
from src.model.base import Base
from src.my_logger.logger import CustomLogger

log = CustomLogger(__name__).get_logger("DEBUG")


class PostgreSQLDatabase(DatabaseInterface):
    """
    This class provides a PostgreSQL implementation of the DatabaseInterface using sqlalchemy_utils.
    """

    def __init__(self, **kwargs):
        """
        Initialize the PostgreSQLDatabase.
        :param kwargs: (dict) The keyword arguments for the PostgreSQL database.
        """
        self._db_name = kwargs.get("db_name")
        user = kwargs.get("user")
        password = kwargs.get("password")
        host = kwargs.get("host")
        port = kwargs.get("port")

        if not database_exists(f"postgresql://{user}:{password}@{host}:{port}/{self._db_name}"):
            create_database(f"postgresql://{user}:{password}@{host}:{port}/{self._db_name}")

        self.engine = create_engine(
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{self._db_name}")
        self.session = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(self.engine)

    def connect(self) -> Connection:
        """
        Connect to the PostgreSQL database.
        :return: (Connection) The SQLAlchemy connection for the PostgreSQL database.
        """
        return self.engine.connect()

    def get_session(self) -> scoped_session:
        """
        Get a session from the PostgreSQL database.  .
        :return: (scoped_session) The SQLAlchemy session for the PostgreSQL database.
        """
        return self.session

