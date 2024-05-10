#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, subqueryload

from crud_repository.db.factory import DatabaseFactory
from crud_repository.model.base import Base
from crud_repository.my_logger.logger import CustomLogger
from crud_repository.repo.repository import Repository
from tests.models import User, Email

log = CustomLogger(__name__).get_logger("DEBUG")


class TestMySQLDBIntegration(unittest.TestCase):
    db_url = (f'mysql+pymysql://'
              f'{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}@'
              f'{os.getenv("MYSQL_HOST")}:{os.getenv("MYSQL_PORT")}/testdb')
    # Create a new database session for each test
    db_config = {
        "type": "mysql",
        "db_name": "testdb",
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "host": os.getenv("MYSQL_HOST"),
        "port": os.getenv("MYSQL_PORT")
    }

    @classmethod
    def setUpClass(cls):
        try:
            engine = create_engine(cls.db_url)
            # Create the database and the table
            with engine.connect() as conn:
                conn.execute(text("CREATE DATABASE IF NOT EXISTS testdb"))
            Base.metadata.create_all(engine)
        except Exception as e:
            log.error(f"Error creating database: {e}")

    def setUp(self):
        log.debug(f"db_config: {self.db_config}")
        # Create a new database session for each test
        self.db = DatabaseFactory.create(self.db_config)
        self.session = self.db.get_scoped_session()
        self.user_repo = Repository(self.db, User)
        self.email_repo = Repository(self.db, Email)
        # Begin a transaction for each test
        self.session.begin_nested()

    @classmethod
    def tearDownClass(cls):
        # Drop the database after all tests are done
        try:
            engine = create_engine(cls.db_url)
            with engine.connect() as conn:
                conn.execute(text("DROP DATABASE IF EXISTS testdb"))
        except Exception as e:
            log.error(f"Error dropping database: {e}")

    def tearDown(self):
        self.session.close()

    def test_connection(self):
        connection = self.db.connect()
        self.assertIsNotNone(connection)
        connection.close()

    def test_database_session(self):
        self.assertIsNotNone(self.db.get_scoped_session())

    def test_create_user_with_emails(self):
        with Session(self.db.engine) as session:
            email1 = Email(email="test1@example.com")
            email2 = Email(email="test2@example.com")
            new_user = User(
                username="test_user", password="test_password",
                emails=[email1, email2],
                name="Test User"

            )
            session.add_all([email1, email2, new_user])
            log.debug(f"New User: {new_user.__dict__}")
            session.commit()

            # Eager Loading Options:
            # created_user = session.query(User) \
            #     .options(joinedload(User.emails)) \
            #     .filter(User.id == new_user.id) \
            #     .one()
            # log.debug(f"Joined Query New User: {new_user.__dict__}")

            # OR (in some cases subqueryload might be better)
            created_user = session.query(User)\
                .options(subqueryload(User.emails))\
                .filter(User.id == new_user.id)\
                .one()
            log.debug(f"SubQuery New User: {created_user.__dict__}")

            # Assert the user and associated emails were created
            self.assertIsNotNone(created_user)
            self.assertEqual(created_user.username, "test_user")
            self.assertEqual(len(created_user.emails), 2)  # Check 2 emails
            self.assertEqual(created_user.emails[0].email, "test1@example.com")
            self.assertEqual(created_user.emails[1].email, "test2@example.com")

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
