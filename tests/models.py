#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Optional
from sqlalchemy import Column, Sequence, Integer, String, ForeignKey
from crud_repository.model.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from crud_repository.my_logger.logger import CustomLogger

log = CustomLogger(__name__).get_logger("DEBUG")


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
    username: Mapped[str] = Column(String(128))
    password: Mapped[Optional[str]] = Column(String(128))
    name: Mapped[str] = Column(String(30))
    fullname: Mapped[Optional[str]] = Column(String(30))
    emails: Mapped[List["Email"]] = relationship(
        "Email", back_populates="user", cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "fullname": self.fullname,
            "username": self.username,
            "password": self.password,
            "emails": [email.as_dict() for email in self.emails] if self.emails is not None else [],
        }

    def as_dict(self) -> dict:  # renamed from __dict__ to as_dict
        return self.to_dict()

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r}, "
            f"username={self.username!r}, password={self.password!r}, emails={self.emails!r})"
        )


class Email(Base):
    __tablename__ = "email"
    id: Mapped[int] = Column(
        Integer,
        Sequence("email_id_seq"),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
        index=True,
    )
    email: Mapped[str] = Column(String(30))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(
        "User", back_populates="emails"
    )

    def to_dict(self) -> dict:
        return {"id": self.id, "email": self.email}

    def as_dict(self) -> dict:  # renamed from __dict__ to as_dict
        return self.to_dict()

    def __repr__(self) -> str:
        return f"Email(id={self.id!r}, email_address={self.email!r})"
