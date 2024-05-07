#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides classes for managing databases.
"""
import sys
import traceback

from sqlalchemy import create_engine, Connection, sql
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from src.db.idatabase import IDatabase
from src.model.base import Base
from src.my_logger.logger import CustomLogger

log = CustomLogger(__name__).get_logger("DEBUG")


# ---------------------------------------------------------
class MySQLDatabase(IDatabase):
    """
    This class provides a MySQL implementation of the Database.
    """

    def __init__(self, **kwargs):
        """
        Initialize the MySQLDatabase.
        :param kwargs: (dict) The keyword arguments for the PostgreSQL database.
        """
        try:
            db_name = kwargs.get("db_name", None)
            user = kwargs.get("user", None)
            password = kwargs.get("password", None)
            host = kwargs.get("host", None)
            port = kwargs.get("port", None)
            url = kwargs.get("url", f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}")
            # Create the database if it doesn't exist
            if not database_exists(url):
                create_database(url)
            # Create the engine and session
            self.engine = create_engine(url)
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


