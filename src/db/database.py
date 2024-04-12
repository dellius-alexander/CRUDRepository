#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import psycopg2
import pymysql
from psycopg2 import sql
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from src.model.base import Base
from src.myLogger.Logger import get_logger

log = get_logger(__name__)


# ---------------------------------------------------------
class DatabaseInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_session(self) -> Session:
        pass

    def __dict__(self):
        return {
            'engine': self.engine,
            'session': self.Session
        }

    def __repr__(self):
        return f"PostgreSQLDatabase(engine={self.engine!r}, session={self.Session!r})"


# ---------------------------------------------------------
class PostgreSQLDatabase(DatabaseInterface):
    def __init__(self, db_name, user, password, host, port):
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(database="postgres", user=user, password=password, host=host)

        conn.autocommit = True

        # Create a new cursor
        cursor = conn.cursor()

        # Check if the database exists
        query = sql.SQL("SELECT 1 FROM 'pg_database' WHERE 'datname' = {0}".format(db_name))
        cursor.execute(query)

        # If it doesn't exist, create it
        if cursor.fetchone() is None:
            cursor.execute(sql.SQL("CREATE DATABASE {0}".format(db_name)))
            # log.info(f"""Database {db_name} created successfully\n""")

        # Close the cursor and the connection
        cursor.close()
        conn.close()

        self.engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
        self.Session = scoped_session(session_factory=sessionmaker(bind=self.engine))
        # Add these lines to create all tables
        Base.metadata.create_all(self.engine)

    def connect(self):
        return self.engine.connect()

    def get_session(self) -> Session:
        return self.Session


# ---------------------------------------------------------
class MySQLDatabase(DatabaseInterface):
    def __init__(self, db_name, user, password, host, port):
        # Connect to the MySQL server
        if not MySQLDatabase.database_exists(user, password, host, port, db_name):
            MySQLDatabase.create_database(user, password, host, port, db_name)

        self.engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}')
        self.Session = scoped_session(session_factory=sessionmaker(bind=self.engine))

        # Add these lines to create all tables
        Base.metadata.create_all(self.engine)

    @staticmethod
    def database_exists(user, password, host, port, db_name):
        conn = pymysql.connect(user=user, password=password, host=host, port=int(port))
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        conn.close()
        return db_name in databases

    @staticmethod
    def create_database(user, password, host, port, db_name):
        conn = pymysql.connect(user=user, password=password, host=host, port=int(port))
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {db_name}")
        conn.commit()
        conn.close()

    def connect(self):
        return self.engine.connect()

    def get_session(self) -> Session:
        return self.Session


# ---------------------------------------------------------
class MariaDBDatabase(DatabaseInterface):
    def __init__(self, db_name, user, password, host, port):
        # # Connect to the MariaDB server
        # if not MariaDBDatabase.database_exists(user, password, host, port, db_name):
        #     MariaDBDatabase.create_database(user, password, host, port, db_name)

        self.engine = create_engine(f'mariadb+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4')
        self.Session = scoped_session(session_factory=sessionmaker(bind=self.engine))

        # Check if the database exists and create it if it doesn't
        connection = self.engine.raw_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            connection.commit()
        except pymysql.err.ProgrammingError as e:
            # Ignore errors if the database already exists
            if e.args[0] != 1007:  # 1007 is the error code for "Database exists"
                raise
        finally:
            cursor.close()
            connection.close()

        # Add these lines to create all tables
        Base.metadata.create_all(self.engine)

    def connect(self):
        return self.engine.connect()

    def get_session(self) -> Session:
        return self.Session


# ---------------------------------------------------------
class DatabaseFactory:
    @staticmethod
    def create_database(config: dict):
        if config['type'] == 'postgresql':
            return PostgreSQLDatabase(config['db_name'], config['user'], config['password'], config['host'],
                                      config['port'])
        elif config['type'] == 'mysql':
            return MySQLDatabase(config['db_name'], config['user'], config['password'], config['host'],
                                 config['port'])
        elif config['type'] == 'mariadb':
            return MariaDBDatabase(config['db_name'], config['user'], config['password'], config['host'],
                                   config['port'])
        # ... other database types
        raise ValueError('Invalid database type')


# ---------------------------------------------------------

