#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
from sqlalchemy import create_engine, text

from src.repo.repository import Repository
from src.db.factory import DatabaseFactory
from src.model.base import Base
from tests.user import User
from src.my_logger.logger import CustomLogger

log = CustomLogger(__name__).get_logger("DEBUG")


class TestPostgresDBIntegration(unittest.TestCase):
    db_url = (f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}'
              f'@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_HOST")}/{os.getenv("POSTGRES_DB")}')
    db_config = {
        "type": "postgresql",
        "db_name": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("POSTGRES_PORT"),
        "url": db_url,
    }
    database_dropped = False

    @classmethod
    def setUpClass(cls):
        try:
            engine = create_engine(cls.db_url)
            # Create the database and the table
            with engine.connect() as conn:
                conn.execute(text("CREATE DATABASE test_db;"))
            Base.metadata.create_all(engine)
        except Exception as e:
            log.error(f"Error creating database: {e}")

    def setUp(self):
        log.debug(f"db_config: {self.db_config}")
        # Create a new database session for each test
        self.db = DatabaseFactory.create(self.db_config)
        # Create a repository for the User model
        self.user_repo = Repository(self.db, User)
        self.session = self.db.get_session()
        # Begin a transaction for each test
        self.session.begin_nested()

    @classmethod
    def tearDownClass(cls):
        if not cls.database_dropped:
            try:
                engine = create_engine(cls.db_url)
                with engine.connect() as conn:
                    conn.execute(text("DROP DATABASE IF EXISTS test_db"))
                cls.database_dropped = True
            except Exception as e:
                log.error(f"Error dropping database: {e}")

    def tearDown(self):
        self.session.close()

    def test_connect(self):
        # Test the connect method
        connection = self.db.connect()
        self.assertIsNotNone(connection)
        log.debug(f"Connection: {connection.__dict__}")

    def test_get_session(self):
        # Test the get_session method
        session = self.db.get_session()
        self.assertIsNotNone(session)
        log.debug(f"Session: {session}")

    def test_create_user(self):
        new_user = User(username="test_user", password="test_password")
        self.user_repo.create(new_user)
        log.debug(f"New User: {new_user.__dict__}")
        # Assert that the user was created successfully
        created_user = self.user_repo.read(new_user.id)
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, "test_user")
        self.assertEqual(created_user.password, "test_password")
        log.debug(f"""
        Created User: {created_user.__dict__}
        """)

    def test_read_user(self):
        # Create a user
        new_user = User(username="test_user_read", password="test_password_read")
        self.user_repo.create(new_user)
        log.debug(f"New User: {new_user.__dict__}")
        # Read the user by ID
        read_user = self.user_repo.read(new_user.id)

        # Assert that the read user matches the created user
        self.assertIsNotNone(read_user)
        self.assertEqual(read_user.username, "test_user_read")
        self.assertEqual(read_user.password, "test_password_read")
        log.debug(f"""
        Read User: {read_user.__dict__}
        """)

    def test_update_user(self):
        # Create a user
        new_user = User(username="test_user_update", password="test_password_update")
        self.user_repo.create(new_user)
        log.debug(f"New User: {new_user.__dict__}")
        # Update the user's password
        updated_password = "updated_password"
        new_user.password = updated_password
        self.user_repo.update(new_user)

        # Read the updated user from the database
        updated_user = self.user_repo.read(new_user.id)

        # Assert that the password was updated successfully
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.password, updated_password)
        log.debug(f"Updated User: {updated_user.__dict__}")

    def test_delete_user(self):
        # Create a user
        new_user = User(username="test_user_delete", password="test_password_delete")
        self.user_repo.create(new_user)
        log.debug(f"New User: {new_user.__dict__}")
        # Delete the user
        self.user_repo.delete(new_user)

        # Assert that the user no longer exists in the database
        deleted_user = self.user_repo.read(new_user.id)
        self.assertIsNone(deleted_user)
        log.debug(f"Deleted User: {deleted_user}")


if __name__ == "__main__":
    unittest.main()
