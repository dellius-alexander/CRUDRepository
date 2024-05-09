from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, ForeignKeyConstraint
from sqlalchemy.orm import relationship, Mapped
from crud_repository.model.base import Base


# ---------------------------------------------------------
class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = Column(Integer, primary_key=True)
    street: Mapped[str] = Column(String(100), nullable=False)
    city: Mapped[str] = Column(String(50), nullable=False)
    state: Mapped[str] = Column(String(20), nullable=False)
    zipcode: Mapped[str] = Column(String(10), nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # users = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address(id={self.id}, street='{self.street}', city='{self.city}', state='{self.state}', zipcode='{self.zipcode}', last_updated='{self.last_updated}')"

    def to_dict(self):
        return {
            'id': self.id,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'last_updated': self.last_updated
        }


# ---------------------------------------------------------
class Role(Base):
    __tablename__ = 'role'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(50), nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"Role(id={self.id}, name='{self.name}', last_updated='{self.last_updated}')"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_updated': self.last_updated
        }


# ---------------------------------------------------------
class Email(Base):
    __tablename__ = 'email'

    id: Mapped[int] = Column(Integer, primary_key=True)
    email: Mapped[str] = Column(String(200), nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # users = relationship("User", back_populates="email")

    def __repr__(self):
        return f"Email(id={self.id}, email='{self.email}', last_updated='{self.last_updated}')"

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'last_updated': self.last_updated
        }


# ---------------------------------------------------------
class User(Base):
    """
    User model

    Attributes:
    -----------
    id: int
         User id
    username: str
            Username
    password: str
            User password
    email_id: int
            Email id
    address_id: int
            Address id
    role_id: int
            Role id
    last_updated: datetime
            Last updated datetime
    """
    __tablename__ = 'user'

    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String(50), nullable=False)
    password: Mapped[str] = Column(String(100), nullable=False)
    email_id: Mapped[Email] = Column(Integer, ForeignKey('emails.id'), ForeignKeyConstraint(columns=['email_id'], refcolumns=['emails.id'], use_alter=True, name='fk_email_id'))
    address_id: Mapped[Address] = Column(Integer, ForeignKey('addresses.id'), nullable=True)
    role_id: Mapped[Role] = Column(Integer, ForeignKey('roles.id'), nullable=True)
    last_updated: Mapped[DateTime] = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    email = relationship("Email", back_populates="users")
    address = relationship("Address", back_populates="users")
    role = relationship("Role", back_populates="users")

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', password='{self.password}', email_id='{self.email_id}', address_id='{self.address_id}', role_id='{self.role_id}', last_updated='{self.last_updated}')"

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email_id': self.email_id,
            'address_id': self.address_id,
            'role_id': self.role_id,
            'last_updated': self.last_updated
        }


# ---------------------------------------------------------
def test_user():

    user = User(id=1, username='test', password='test')
    print(user.__dict__)
    # assert user.__repr__() == "User(id=1, username='test', password='test', last_updated='')"


