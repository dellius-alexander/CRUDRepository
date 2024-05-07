#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides classes for managing databases.
"""
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
    @staticmethod
    def create(config: dict) -> IDatabase:
        """
        Create a database instance based on the provided configuration.

        :param config: The configuration for the database.
        :return: (IDatabase) The created database instance.
        """
        try:
            # Create the appropriate database instance based on the configuration
            # (e.g., PostgreSQL, MySQL, MariaDB, etc.)
            if config["type"] == "postgresql":
                return PostgreSQLDatabase(
                    **{
                        "db_name": config["db_name"],
                        "user": config["user"],
                        "password": config["password"],
                        "host": config["host"],
                        "port": config["port"],
                    }
                )
            if config["type"] == "mysql":
                return MySQLDatabase(
                    **{
                        "db_name": config["db_name"],
                        "user": config["user"],
                        "password": config["password"],
                        "host": config["host"],
                        "port": config["port"],
                    }
                )
            if config["type"] == "mariadb":
                return MariaDBDatabase(
                    **{
                        "db_name": config["db_name"],
                        "user": config["user"],
                        "password": config["password"],
                        "host": config["host"],
                        "port": config["port"],
                    }
                )
            # ... other database types
            raise ValueError("Invalid database type")
        except Exception as e:
            log.debug(f"Error creating database instance: {e}")
            raise e
