#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides classes for managing databases.
"""
from abc import ABC, abstractmethod
import psycopg2
import pymysql
from psycopg2 import sql
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from src.model.base import Base
from src.myLogger.Logger import get_logger

log = get_logger(__name__)


# ---------------------------------------------------------
class DatabaseInterface(ABC):
    """
    This class defines the interface for a database.

    Attributes:
        engine (Engine): The SQLAlchemy engine for the database.
        session (Session): The SQLAlchemy session for the database.
    """

    session: Session
    engine: Engine

    @abstractmethod
    def connect(self):
        """
        Connect to the database.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def get_session(self) -> Session:
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

class PostgreSQLDatabase(DatabaseInterface):
    """
    This class provides a PostgreSQL implementation of the DatabaseInterface.

    Attributes:
        engine (Engine): The SQLAlchemy engine for the PostgreSQL database.
        session (Session): The SQLAlchemy session for the PostgreSQL database.
    """

    def __init__(self, db_name: str, user: str, password: str, host: str, port: str):
        """
        Initialize the PostgreSQLDatabase.

        Parameters:
            db_name (str): The name of the PostgreSQL database.
            user (str): The username for the PostgreSQL database.
            password (str): The password for the PostgreSQL database.
            host (str): The host of the PostgreSQL database.
            port (str): The port of the PostgreSQL database.
        """
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(
            database="postgres", user=user, password=password, host=host
        )

        conn.autocommit = True

        # Create a new cursor
        cursor = conn.cursor()

        # Check if the database exists
        query = sql.SQL(
            "SELECT 1 FROM 'pg_database' WHERE 'datname' = {0}".format(db_name)
        )
        cursor.execute(query)

        # If it doesn't exist, create it
        if cursor.fetchone() is None:
            cursor.execute(sql.SQL("CREATE DATABASE {0}".format(db_name)))
            # log.info(f"""Database {db_name} created successfully\n""")

        # Close the cursor and the connection
        cursor.close()
        conn.close()

        self.engine = create_engine(
            f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        )
        self.session = scoped_session(session_factory=sessionmaker(bind=self.engine))
        # Add these lines to create all tables
        Base.metadata.create_all(self.engine)

    def connect(self):
        """
        Connect to the PostgreSQL database.
        """
        self.engine.connect()

    def get_session(self) -> Session:
        """
        Get a session from the PostgreSQL database.

        Returns:
            Session: The SQLAlchemy session for the PostgreSQL database.
        """
        return self.session()


# ---------------------------------------------------------
class MySQLDatabase(DatabaseInterface):
    """
    This class provides a MySQL implementation of the DatabaseInterface.

    Attributes:
        engine (Engine): The SQLAlchemy engine for the MySQL database.
        session (Session): The SQLAlchemy session for the MySQL database.
    """

    def __init__(self, db_name: str, user: str, password: str, host: str, port: str):
        """
        Initialize the MySQLDatabase.

        Parameters:
            db_name (str): The name of the MySQL database.
            user (str): The username for the MySQL database.
            password (str): The password for the MySQL database.
            host (str): The host of the MySQL database.
            port (str): The port of the MySQL database.
        """
        # Connect to the MySQL server
        if not MySQLDatabase.database_exists(user, password, host, port, db_name):
            MySQLDatabase.create_database(user, password, host, port, db_name)

        self.engine = create_engine(
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
        )
        self.session = scoped_session(session_factory=sessionmaker(bind=self.engine))

        # Add these lines to create all tables
        Base.metadata.create_all(self.engine)

    @staticmethod
    def database_exists(user, password, host, port, db_name):
        conn = pymysql.connect(user=user, password=password, host=host, port=int(port))
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        conn.close()
        return db_name in databases

    @staticmethod
    def create_database(user, password, host, port, db_name):
        conn = pymysql.connect(user=user, password=password, host=host, port=int(port))
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {db_name}")
        conn.commit()
        conn.close()

    def connect(self):
        """
        Connect to the MySQL database.
        """
        self.engine.connect()

    def get_session(self) -> Session:
        """
        Get a session from the MySQL database.

        Returns:
            Session: The SQLAlchemy session for the MySQL database.
        """
        return self.session


# ---------------------------------------------------------
class MariaDBDatabase(DatabaseInterface):
    """
    This class provides a MariaDB implementation of the DatabaseInterface.

    Attributes:
        engine (Engine): The SQLAlchemy engine for the MariaDB database.
        session (Session): The SQLAlchemy session for the MariaDB database.
    """

    def __init__(self, db_name: str, user: str, password: str, host: str, port: str):
        """
        Initialize the MariaDBDatabase.

        Parameters:
            db_name (str): The name of the MariaDB database.
            user (str): The username for the MariaDB database.
            password (str): The password for the MariaDB database.
            host (str): The host of the MariaDB database.
            port (str): The port of the MariaDB database.
        """

        self.engine = create_engine(
            f"mariadb+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4"
        )
        self.session = scoped_session(session_factory=sessionmaker(bind=self.engine))

        # Check if the database exists and create it if it doesn't
        connection = self.engine.raw_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            connection.commit()
        except pymysql.err.ProgrammingError as e:
            # Ignore errors if the database already exists
            if e.args[0] != 1007:  # 1007 is the error code for "Database exists"
                raise
        finally:
            cursor.close()
            connection.close()

        # Add these lines to create all tables
        Base.metadata.create_all(self.engine)

    def connect(self):
        """
        Connect to the MariaDB database.
        """
        self.engine.connect()

    def get_session(self) -> Session:
        """
        Get a session from the MariaDB database.

        Returns:
            Session: The SQLAlchemy session for the MariaDB database.
        """
        return self.session

# ---------------------------------------------------------

class DatabaseFactory:
    """
    This class provides a factory for creating database instances.
    """

    @staticmethod
    def create_database(config: dict) -> DatabaseInterface:
        """
        Create a database instance based on the provided configuration.

        Parameters:
            config (dict): The configuration for the database.

        Returns:
            DatabaseInterface: The created database instance.
        """
        if config["type"] == "postgresql":
            return PostgreSQLDatabase(
                config["db_name"],
                config["user"],
                config["password"],
                config["host"],
                config["port"],
            )
        elif config["type"] == "mysql":
            return MySQLDatabase(
                config["db_name"],
                config["user"],
                config["password"],
                config["host"],
                config["port"],
            )
        elif config["type"] == "mariadb":
            return MariaDBDatabase(
                config["db_name"],
                config["user"],
                config["password"],
                config["host"],
                config["port"],
            )
        # ... other database types
        raise ValueError("Invalid database type")


# ---------------------------------------------------------
