from sqlalchemy import Column, Boolean, DateTime, Integer, String, text

import base64
import os

from .meta import Base


def generate_token():
    return base64.urlsafe_b64encode(os.urandom(12)).decode("utf-8")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    last_login = Column(DateTime)
    auth_token = Column(String, default=generate_token, unique=True)
    password = Column(String)
    salt = Column(String)
    last_invite = Column(DateTime)
    agreed_tos = Column(DateTime)
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    is_validated = Column(Boolean, nullable=False, server_default="0")

    @property
    def organizations(self):
        result = []
        for has_organization in self.has_organizations:
            result.append(has_organization.organization)
        return result

    @property
    def root_organizations(self):
        working = [h.organization for h in self.has_organizations]
        result = []
        while len(working) > 0:
            current = working.pop()
            if current.parent:
                working.append(current.parent)
            elif current not in result:
                result.append(current)
        return result

    def ensure_token_exists(self):
        if not self.auth_token:
            self.auth_token = generate_token()

    def new_token(self):
        self.auth_token = generate_token()

    @property
    def display_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.first_name or self.last_name or self.email

    @property
    def needs_password(self):
        for has_organization in self.has_organizations:
            if has_organization.permission != "member":
                return True
        return False
