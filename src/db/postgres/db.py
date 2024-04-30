#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides classes for managing databases.
"""
from sqlalchemy import create_engine, Connection, text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database

from src.db.idatabase import IDatabase
from src.model.base import Base
from src.my_logger.logger import CustomLogger

log = CustomLogger(__name__).get_logger("DEBUG")


class PostgreSQLDatabase(IDatabase):
    """
    This class provides a PostgreSQL implementation of the Database using sqlalchemy_utils.
    """

    def __init__(self, **kwargs):
        """
        Initialize the PostgreSQLDatabase.
        :param kwargs: (dict) The keyword arguments for the PostgreSQL database.
        """
        db_name = kwargs.get("db_name", None)
        user = kwargs.get("user", None)
        password = kwargs.get("password", None)
        host = kwargs.get("host", None)
        port = kwargs.get("port", None)
        url = kwargs.get("url", f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}")
        # Create the database if it doesn't exist
        if not database_exists(url):
            create_database(url)
        # Create the engine and session
        self.engine = create_engine(url)
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
