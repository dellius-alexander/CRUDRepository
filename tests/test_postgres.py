#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from src.model.base import Base
from src.db.database import DatabaseFactory
from tests.user import User
from tests.repository import UserRepository


class TestPostgresImplementation(unittest.TestCase):
    def setUp(self):
        # Set up test database
        config = {
            "type": "postgresql",
            "db_name": "test_db",
            "user": "my_user",
            "password": "postgrespassword",
            "host": "10.0.0.223",
            "port": "5432",
        }

        self.db = DatabaseFactory.create_database(config)
        self.user_repo = UserRepository(self.db)

        # Create tables
        # Base.metadata.create_all(self.db.engine)

    def tearDown(self):
        # Drop tables
        Base.metadata.drop_all(self.db.engine)

        # Close the database connection
        self.db.engine.dispose()

    def test_connect(self):
        # Test the connect method
        connection = self.db.connect()
        self.assertIsNotNone(connection)

    def test_get_session(self):
        # Test the get_session method
        session = self.db.get_session()
        self.assertIsNotNone(session)

    def test_create_user(self):
        new_user = User(username="test_user", password="test_password")
        self.user_repo.create(new_user)

        # Assert that the user was created successfully
        created_user = self.user_repo.read(new_user.id)
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, "test_user")
        self.assertEqual(created_user.password, "test_password")

    def test_read_user(self):
        # Create a user
        new_user = User(username="test_user_read", password="test_password_read")
        self.user_repo.create(new_user)

        # Read the user by ID
        read_user = self.user_repo.read(new_user.id)

        # Assert that the read user matches the created user
        self.assertIsNotNone(read_user)
        self.assertEqual(read_user.username, "test_user_read")
        self.assertEqual(read_user.password, "test_password_read")

    def test_update_user(self):
        # Create a user
        new_user = User(username="test_user_update", password="test_password_update")
        self.user_repo.create(new_user)

        # Update the user's password
        updated_password = "updated_password"
        new_user.password = updated_password
        self.user_repo.update(new_user)

        # Read the updated user from the database
        updated_user = self.user_repo.read(new_user.id)

        # Assert that the password was updated successfully
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.password, updated_password)

    def test_delete_user(self):
        # Create a user
        new_user = User(username="test_user_delete", password="test_password_delete")
        self.user_repo.create(new_user)

        # Delete the user
        self.user_repo.delete(new_user)

        # Assert that the user no longer exists in the database
        deleted_user = self.user_repo.read(new_user.id)
        self.assertIsNone(deleted_user)


if __name__ == "__main__":
    unittest.main()
