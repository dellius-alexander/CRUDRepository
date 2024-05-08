#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides classes for managing databases.
"""
from typing import Dict, Type

from crud_repository.db.idatabase import IDatabase
from crud_repository.db.mariadb.db import MariaDBDatabase
from crud_repository.db.mysql.db import MySQLDatabase
from crud_repository.db.postgres.db import PostgreSQLDatabase
from crud_repository.my_logger.logger import CustomLogger

log = CustomLogger(__name__).get_logger("DEBUG")


# ---------------------------------------------------------
class DatabaseFactory:
    """
    This class provides a factory for creating database instances.
    """
    _instances: Dict = {}

    @staticmethod
    def create(config: dict) -> Type[IDatabase]:
        """
        Create a database instance based on the provided configuration.

        :param config: The configuration for the database.
        :return: (IDatabase) The created database instance.
        """
        try:
            # Check if an instance of this type already exists
            if config["type"] in DatabaseFactory._instances:
                return DatabaseFactory._instances[config["type"]]

            # Create the appropriate database instance based on the configuration
            # (e.g., PostgreSQL, MySQL, MariaDB, etc.)
            if config["type"].lower() == "postgresql":
                instance = PostgreSQLDatabase(
                    **{
                        "db_name": config["db_name"],
                        "user": config["user"],
                        "password": config["password"],
                        "host": config["host"],
                        "port": config["port"],
                    }
                )
            elif config["type"].lower() == "mysql":
                instance = MySQLDatabase(
                    **{
                        "db_name": config["db_name"],
                        "user": config["user"],
                        "password": config["password"],
                        "host": config["host"],
                        "port": config["port"],
                    }
                )
            elif config["type"].lower() == "mariadb":
                instance = MariaDBDatabase(
                    **{
                        "db_name": config["db_name"],
                        "user": config["user"],
                        "password": config["password"],
                        "host": config["host"],
                        "port": config["port"],
                    }
                )
            else:
                raise ValueError("Invalid database type")

            # Store the new instance in the dictionary
            DatabaseFactory._instances[config["type"]] = instance

            return instance
        except Exception as e:
            log.debug(f"Error creating database instance: {e}")
            raise e