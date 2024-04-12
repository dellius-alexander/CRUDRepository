#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from tests.repository import UserRepository
from src.db.database import DatabaseFactory
from tests.user import User
from src.model.base import Base


class TestMariaDB(unittest.TestCase):
    def setUp(self):
        # Create a new database instance
        db_config = {
            "type": "mariadb",
            "db_name": "volunteer",
            "user": "root",
            "password": "adminpassword",
            "host": "10.0.0.223",
            "port": "3307",
        }

        self.database = DatabaseFactory.create_database(db_config)
        self.user_repository = UserRepository(self.database)

        # # Create the User table
        # Base.metadata.create_all(self.database.engine)

    def tearDown(self):
        # Clean up the database after each test
        session = self.database.get_session()
        session.query(User).delete()
        session.commit()
        session.close()

        # Drop the User table
        Base.metadata.drop_all(self.database.engine)

    def test_create_user(self):
        new_user = User(username="testuser", password="testpassword")
        created_user = self.user_repository.create(new_user)

        self.assertIsNotNone(created_user)
        self.assertEqual(created_user["username"], "testuser")
        self.assertEqual(created_user["password"], "testpassword")

    def test_read_user(self):
        new_user = User(username="testuser", password="testpassword")
        created_user = self.user_repository.create(new_user)

        read_user = self.user_repository.read(created_user["id"])

        self.assertIsNotNone(read_user)
        self.assertEqual(read_user.id, created_user["id"])
        self.assertEqual(read_user.username, "testuser")
        self.assertEqual(read_user.password, "testpassword")

    def test_update_user(self):
        new_user = User(username="testuser", password="testpassword")
        created_user = self.user_repository.create(new_user)

        updated_username = "updateduser"
        updated_password = "updatedpassword"
        created_user.username = updated_username
        created_user.password = updated_password

        self.user_repository.update(created_user)

        read_user = self.user_repository.read(created_user.id)

        self.assertIsNotNone(read_user)
        self.assertEqual(read_user.id, created_user.id)
        self.assertEqual(read_user.username, updated_username)
        self.assertEqual(read_user.password, updated_password)

    def test_delete_user(self):
        new_user = User(username="testuser", password="testpassword")
        created_user = self.user_repository.create(new_user)

        self.user_repository.delete(created_user)

        read_user = self.user_repository.read(created_user.id)

        self.assertIsNone(read_user)


if __name__ == "__main__":
    unittest.main()
