#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides classes for managing databases.
"""
import sys
import traceback

import pymysql
from sqlalchemy import create_engine, Engine, Connection
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from db.idatabase import IDatabase
from src.model.base import Base
from src.my_logger.logger import CustomLogger

log = CustomLogger(__name__).get_logger("DEBUG")


# ---------------------------------------------------------
class MariaDBDatabase(IDatabase):
    """
    This class provides a MariaDB implementation of the Database.

    Attributes:
        engine (Engine): The SQLAlchemy engine for the MariaDB database.
        session (Session): The SQLAlchemy session for the MariaDB database.
    """

    def __init__(self, **kwargs):
        """
        Initialize the MariaDBDatabase.
        :param kwargs: (dict) The keyword arguments for the PostgreSQL database.
        """
        try:
            db_name = kwargs.get("db_name")
            user = kwargs.get("user")
            password = kwargs.get("password")
            host = kwargs.get("host")
            port = kwargs.get("port")
            self.engine = create_engine(
                f"mariadb+pymysql://{user}:{password}@{host}:{port}/{db_name}"
            )
            # Create the database if it doesn't exist
            if not database_exists(self.engine.url):
                create_database(self.engine.url)
            # Create the session
            self.session = scoped_session(sessionmaker(bind=self.engine))
            # Add this line to create all tables based on Base class
            Base.metadata.create_all(self.engine)
        except OperationalError as e:
            log.debug(f"Error connecting to MySQL database: {e}")
            traceback.print_exc()
            raise e
        except Exception as e:
            log.debug(f"Error initializing MySQL database: {e}")
            traceback.print_exc()
            sys.exit(1)

    def connect(self) -> Connection:
        """
        Connect to the MariaDB database and return the connection.
        """
        return self.engine.connect()

    def get_session(self) -> scoped_session:
        """
        Get a session from the MariaDB database.
        """
        return self.session
