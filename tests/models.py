from typing import List

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from crud_repository.model.base import Base


# ---------------------------------------------------------
class User(Base):
    """User model class.

    Attributes:
        id: (int) The user id.
        username: (str) The username.
        password: (str) The password.
        name: (str) The name.
        emails: (Optional[List[Email]]) The list of emails.
        addresses: (Optional[List[Address]]) The list of addresses.
        roles: (Optional[List[Role]]) The list of roles.
        last_updated: (DateTime) The last updated date.
    """
    __tablename__ = 'user'

    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String(50), nullable=False)
    password: Mapped[str] = Column(String(100), nullable=False)
    name: Mapped[str] = Column(String(100), nullable=True)
    emails: Mapped[List["Email"]] = relationship(backref='user')

    addresses: Mapped[List["Address"]] = relationship(backref='user')

    roles: Mapped[List["Role"]] = relationship(backref='user')

    last_updated: Mapped[DateTime] = Column(DateTime, name='last_updated', nullable=False, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', password='{self.password}', email_id='{self.email_id}', address_id='{self.address_id}', role_id='{self.role_id}', last_updated='{self.last_updated}')"

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email_id': self.emails,
            'address_id': self.addresses,
            'role_id': self.roles,
            'last_updated': self.last_updated
        }


# ---------------------------------------------------------
class Address(Base):
    """Address model class.

    Attributes:
        id: (int) The address id.
        street: (str) The street address.
        city: (str) The city.
        state: (str) The state.
        zipcode: (str) The zip code.
        last_updated: (DateTime) The last updated date.
    """
    __tablename__ = 'address'

    id: Mapped[int] = Column(Integer, primary_key=True)
    street: Mapped[str] = Column(String(100), nullable=False)
    city: Mapped[str] = Column(String(50), nullable=False)
    state: Mapped[str] = Column(String(20), nullable=False)
    zipcode: Mapped[str] = Column(String(10), nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime, name='last_updated', nullable=False, default=func.now(), onupdate=func.now())

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    # user: Mapped["User"] = relationship()

    def __repr__(self):
        return f"Address(id={self.id}, street='{self.street}', city='{self.city}', state='{self.state}', zipcode='{self.zipcode}', last_updated='{self.last_updated}')"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'last_updated': self.last_updated
        }


# ---------------------------------------------------------
class Role(Base):
    """Role model class.

    Attributes:
        id: (int) The role id.
        name: (str) The role name.
        last_updated: (DateTime) The last updated date.
    """
    __tablename__ = 'role'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(50), nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime, name='last_updated', nullable=False, default=func.now(), onupdate=func.now())

    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"Role(id={self.id}, name='{self.name}', last_updated='{self.last_updated}')"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'last_updated': self.last_updated
        }


# ---------------------------------------------------------
class Email(Base):
    """Email model class.

    Attributes:
        id: (int) The email id.
        email: (str) The email address.
        last_updated: (DateTime) The last updated date.
    """
    __tablename__ = 'email'

    id: Mapped[int] = Column(Integer, primary_key=True)
    email: Mapped[str] = Column(String(200), nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime, name='last_updated', nullable=False, default=func.now(), onupdate=func.now())

    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"Email(id={self.id}, email='{self.email}', last_updated='{self.last_updated}')"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'email': self.email,
            'last_updated': self.last_updated
        }


# ---------------------------------------------------------
