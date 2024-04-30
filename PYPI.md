[![Build test and deploy to package repository](https://github.com/dellius-alexander/CRUDRepository/actions/workflows/deploy.yml/badge.svg)](https://github.com/dellius-alexander/CRUDRepository/actions/workflows/deploy.yml)

---

# CRUD Repository

---
## Description

The CRUDRepository is a Python project designed to provide a 
generic implementation of Create, Read, Update, and Delete (CRUD) 
operations for various databases. It uses the Repository design pattern 
to abstract the data access layer, allowing for easy switching between 
different databases using the Factory pattern in which each database 
object implements a Singleton object.  

The project includes classes for handling different types of databases 
such as PostgreSQL, MySQL, and MariaDB. Each of these classes implements 
a common Interface, ensuring a consistent method of interaction 
regardless of the underlying database.  

The CRUDRepository also includes a Repository class that provides generic 
CRUD operations. This class can be used as a base for creating more specific 
repositories, like the test Repository UserRepository included in the project, which is 
designed to manage User instances.  

The project uses SQLAlchemy for ORM, providing a high-level, Pythonic 
interface for database operations. It also includes a DatabaseFactory for 
creating instances of the appropriate database class based on provided 
configuration.  

In summary, CRUDRepository is a flexible and extensible 
foundation for Python applications that require database interactions, 
abstracting the complexities of direct database access and providing a 
clear and simple interface for performing CRUD operations.

---

## Installation
    
```bash
pip install crud-repository
```

## Code Example Usage

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.db.factory import DatabaseFactory
from typing import Optional
from sqlalchemy import Column, Sequence, Integer, String
from sqlalchemy.orm import Mapped
from src.model.base import Base
from db.idatabase import IDatabase
from src.repo.repository import Repository


# ---------------------------------------------------------
# Create a User model
# ---------------------------------------------------------
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = Column(
        Integer,
        Sequence("user_id_seq"),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
        index=True,
    )
    username: Mapped[str] = Column(String(128), nullable=False)
    password: Mapped[Optional[str]] = Column(String(128), nullable=True)

    def to_dict(self) -> dict:
        return {"id": self.id, "username": self.username, "password": self.password}

    def as_dict(self) -> dict:  # renamed from __dict__ to as_dict
        return self.to_dict()

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, name={self.username!r}, fullname={self.password!r})"
        )


# ---------------------------------------------------------
# Create a UserRepository instance with the database instance
# ---------------------------------------------------------
class UserRepository(Repository[User]):
    def __init__(self, database: IDatabase):
        super().__init__(database, User)


# ---------------------------------------------------------
# Create a new user
# ---------------------------------------------------------
if __name__ == '__main__':
    # Create a new database instance
    db_config = {
        'type': 'postgresql',
        'db_name': 'volunteer',
        'user': "postgres",
        'password': "adminpassword",
        'host': "127.0.0.1",
        'port': "5432"
    }
    # Create a new database instance
    db = DatabaseFactory.create(db_config)

    # Create a UserRepository instance with the database instance
    user_repo = UserRepository(db)

    # OR create a generic Repository instance with the 
    # database instance and the User model
    #user_repo = Repository(db, User)

    # Create a new user
    user = User(username='Candy', password='password')

    # Add the user to the database
    user_repo.create(user)
```
---

