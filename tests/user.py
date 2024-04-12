#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional, List
from sqlalchemy import Column, Sequence, Integer, String
from sqlalchemy.orm import Mapped, relationship
from src.model.base import Base


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
    # addresses: Mapped[List["Address"]] = relationship("Address", back_populates="user")

    def to_dict(self) -> dict:
        return {"id": self.id, "username": self.username, "password": self.password}

    def as_dict(self) -> dict:  # renamed from __dict__ to as_dict
        return self.to_dict()

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, name={self.username!r}, fullname={self.password!r})"
        )
