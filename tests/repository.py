#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db.database import DatabaseInterface
from user import User
from src.repo.repository import Repository


# ---------------------------------------------------------
class UserRepository(Repository[User]):
    def __init__(self, database: DatabaseInterface):
        super().__init__(database, User)
