#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from crud_repository.db.idatabase import IDatabase
from tests.models import User
from crud_repository.repo.repository import Repository


# ---------------------------------------------------------
class UserRepository(Repository[User]):
    def __init__(self, database: IDatabase):
        super().__init__(database, User)
