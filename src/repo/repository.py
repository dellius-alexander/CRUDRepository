#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from src.db.database import DatabaseInterface
from src.model.base import Base
from src.myLogger.Logger import get_logger

T = TypeVar('T', bound=Base)

log = get_logger(__name__)


# ---------------------------------------------------------
class RepositoryInterface(ABC):
    @abstractmethod
    def create(self, entity):
        pass

    @abstractmethod
    def read(self, id):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, entity):
        pass


# ---------------------------------------------------------
class Repository(Generic[T]):
    def __init__(self, database: DatabaseInterface, model: type[T]):
        self.database = database
        self.model = model

    def create(self, entity: T):
        session = self.database.get_session()
        try:
            session.add(entity)
            session.commit()
            return {c.key: getattr(entity, c.key) for c in sqlalchemy.inspect(entity).mapper.column_attrs}
        except SQLAlchemyError as e:
            session.rollback()
            log.error(f"Error creating entity in {self.model.__name__} table: {e}")
            raise e
        finally:
            session.close()

    def read(self, id):
        session = self.database.get_session()
        try:
            return session.get(self.model, id)
        except SQLAlchemyError as e:
            log.error(f"Error reading entity from {self.model.__name__} table: {e}")
            raise e
        finally:
            session.close()

    def update(self, entity: T):
        session = self.database.get_session()
        try:
            session.merge(entity)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            log.error(f"Error updating entity from {entity.__name__} table: {e}")
            raise e
        finally:
            session.close()

    def delete(self, entity: T):
        session = self.database.get_session()
        try:
            session.delete(entity)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            log.error(f"Error deleting entity from {entity.__name__} table: {e}")
            raise e
        finally:
            session.close()

    def __dict__(self):
        return {
            'database': self.database.__dict__(),
            'model': self.model.__name__
        }


# ---------------------------------------------------------
class EncryptionHandler:
    @staticmethod
    def encrypt(value):
        # ... implementation
        pass

    @staticmethod
    def decrypt(value):
        # ... implementation
        pass

