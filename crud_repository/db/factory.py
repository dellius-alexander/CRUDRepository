#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides classes for managing databases.
"""
from typing import Dict
from crud_repository.db.idatabase import IDatabase
from crud_repository.db.mariadb.db import MariaDBDatabase
from crud_repository.db.mysql.db import MySQLDatabase
from crud_repository.db.postgres.db import PostgreSQLDatabase
from crud_repository.model.base import Base
from crud_repository.my_logger.logger import CustomLogger

log = CustomLogger(__name__).get_logger("DEBUG")


# ---------------------------------------------------------
class DatabaseFactory:
    """
    This class provides a factory for creating database instances and ensuring tables are created.
    """
    _instances: Dict[str, IDatabase] = {}

    @staticmethod
    def create(config: dict) -> IDatabase:
        """
        Create a database instance based on the provided configuration and create/update all tables.

        :param config: The configuration for the database.
        :return: The created database instance.
        """
        try:
            db_type = config["type"].lower()

            # Check if an instance of this type already exists
            if db_type in DatabaseFactory._instances:
                return DatabaseFactory._instances[db_type]

            # Create the database instance
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
            raise e

