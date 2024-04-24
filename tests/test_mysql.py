#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
from sqlalchemy import create_engine, text

from db.factory import DatabaseFactory
from src.model.base import Base
from src.my_logger.logger import CustomLogger
from tests.repository import UserRepository
from tests.user import User

log = CustomLogger(__name__).get_logger("DEBUG")


class TestMySQLDatabase(unittest.TestCase):
    db_url = (f'mysql+pymysql://'
              f'{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}@'
              f'{os.getenv("MYSQL_HOST")}:{os.getenv("MYSQL_PORT")}/testdb')

    @classmethod
    def setUpClass(cls):
        try:
            engine = create_engine(cls.db_url)
            # Create the database and the table
            with engine.connect() as conn:
                conn.execute(text("CREATE DATABASE IF NOT EXISTS test_db"))
            Base.metadata.create_all(engine)
        except Exception as e:
            log.error(f"Error creating database: {e}")

    def setUp(self):
        # Create a new database session for each test
        db_config = {
            "type": "mysql",
            "db_name": "testdb",
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
            "host": os.getenv("MYSQL_HOST"),
            "port": os.getenv("MYSQL_PORT")
        }
        log.debug(f"db_config: {db_config}")
        self.db = DatabaseFactory.create(db_config)
        self.session = self.db.get_session()
        self.user_repo = UserRepository(self.db)

    @classmethod
    def tearDownClass(cls):
        # Drop the database after all tests are done
        try:
            engine = create_engine(cls.db_url)
            with engine.connect() as conn:
                conn.execute(text("DROP DATABASE IF EXISTS test_db"))
        except Exception as e:
            log.error(f"Error dropping database: {e}")

    def tearDown(self):
        self.session.close()

    def test_connection(self):
        connection = self.db.connect()
        self.assertIsNotNone(connection)
        connection.close()

    def test_database_session(self):
        self.assertIsNotNone(self.db.get_session())

    def test_create_user(self):
        new_user = User(username="test_user", password="test_password")
        self.user_repo.create(new_user)
        created_user = self.user_repo.read(new_user.id)
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, "test_user")
        self.assertEqual(created_user.password, "test_password")

    def test_read_user(self):
        new_user = User(username="test_user", password="test_password")
        self.user_repo.create(new_user)
        created_user = self.user_repo.read(new_user.id)
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, "test_user")
        self.assertEqual(created_user.password, "test_password")

    def test_update_user(self):
        new_user = User(username="test_user", password="test_password")
        self.user_repo.create(new_user)
        created_user = self.user_repo.read(new_user.id)
        self.assertIsNotNone(created_user)

        created_user.username = "updated_user"
        self.user_repo.update(created_user)

        updated_user = self.user_repo.read(created_user.id)
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.username, "updated_user")
        self.assertEqual(updated_user.password, "test_password")

    def test_delete_user(self):
        new_user = User(username="test_user", password="test_password")
        self.user_repo.create(new_user)
        created_user = self.user_repo.read(new_user.id)
        self.assertIsNotNone(created_user)

        self.user_repo.delete(created_user)
        deleted_user = self.user_repo.read(created_user.id)
        self.assertIsNone(deleted_user)


if __name__ == "__main__":
    unittest.main()
