#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from myLogger.Logger import get_logger
from src.db.database import DatabaseFactory
from test.user import User
from src.repo.repository import UserRepository

log = get_logger(__name__)


# ---------------------------------------------------------
if __name__ == "__main__":
    # Create a new database instance
    db_config = {
        "type": "mysql",
        "db_name": "volunteer",
        "user": "my_user",
        "password": "mysqlpassword",
        "host": "10.0.0.223",
        "port": "3306",
    }
    log.info(f"""Database Config: {db_config}""")
    db = DatabaseFactory.create_database(db_config)
    log.info(f"""Database: {db.__dict__()}""")

    # Create a UserRepository instance with the database instance
    user_repo = UserRepository(db)
    log.info(f"""User Repository: {user_repo.__dict__()}""")

    # Create a new user
    user = User(username="Candy", password="password")
    user_repo.create(user)
    log.info(f"""User: {user}""")
