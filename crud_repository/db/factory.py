#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides classes for managing databases.
"""
import traceback
from typing_extensions import Dict, Annotated
from crud_repository.db.idatabase import IDatabase
from crud_repository.db.mariadb.db import MariaDBDatabase
from crud_repository.db.mysql.db import MySQLDatabase
from crud_repository.db.postgres.db import PostgreSQLDatabase
from crud_repository.my_logger.logger import CustomLogger

log = CustomLogger(__name__).get_logger("DEBUG")


# ---------------------------------------------------------
class DatabaseFactory:
    """
    The factory is a singleton that stores instances of the database types.

    The factory creates a database instance based on the provided configuration and creates or updates all tables.

    Attributes:
        _instances (:dict[`str`, `IDatabase`]): A dictionary of database instances.

    Methods:
        create(config: dict) -> IDatabase: Create a database instance based on the provided configuration and create/update all tables.

    Example:
        >>> db_config = {
            "type": "postgresql",
            "db_name": "mydb",
            "user": "myuser",
            "password": "mypassword",
            "host": "hostname/ip address",
            "port": "5432"
        }
        >>> db = DatabaseFactory.create(db_config)

    Exception:
        ValueError: If the database type is invalid.
        Exception: If an error occurs while creating the database instance.
    """

    _instances: Annotated[Dict[str, IDatabase], "A dictionary of database instances."] = {}

    @staticmethod
    def create(config: dict) -> IDatabase:
        """
        Create a database instance based on the provided configuration and create/update all tables.

        :param config: The configuration for the database.
        :return: The created database instance.
        :exception ValueError: If the database type is invalid.
        :exception Exception: If an error occurs while creating the database instance.
        """
        try:
            # Get the database type from the configuration
            db_type = config["type"].lower()

            # Check if an instance of this type already exists
            if db_type in DatabaseFactory._instances:
                # Return the existing instance
                return DatabaseFactory._instances[db_type]

            # Create the database instance based on the type
            instance: IDatabase
            if db_type == "postgresql":
                instance = PostgreSQLDatabase(**config)
            elif db_type == "mysql":
                instance = MySQLDatabase(**config)
            elif db_type == "mariadb":
                instance = MariaDBDatabase(**config)
            else:
                log.debug(f"Invalid database type: {db_type}")
                raise ValueError("Invalid database type: %s" % db_type)

            # Store the new instance in the dictionary
            DatabaseFactory._instances[db_type] = instance
            return instance
        except Exception as e:
            log.debug(f"Error creating database instance: {e}")
            traceback.print_exc()
            raise e

