from sqlalchemy import Column, DateTime, Integer, String, text

from .meta import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    last_login = Column(DateTime)
    auth_token = Column(String)
    password = Column(String)
    salt = Column(String)
