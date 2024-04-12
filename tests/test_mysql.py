#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from tests.repository import UserRepository
from src.db.database import DatabaseFactory
from tests.user import User


class TestDatabase(unittest.TestCase):
    def setUp(self):
        db_config = {
            "type": "mysql",
            "db_name": "volunteer",
            "user": "my_user",
            "password": "mysqlpassword",
            "host": "10.0.0.223",
            "port": "3306",
        }

        self.db = DatabaseFactory.create_database(db_config)
        self.session = self.db.get_session()
        self.user_repo = UserRepository(self.db)

    def tearDown(self):
        self.session.close()

    def test_connection(self):
        connection = self.db.connect()
        self.assertIsNotNone(connection)
        connection.close()

    def test_database_session(self):
        self.assertIsNotNone(self.session)

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
