from sqlalchemy import Column, ForeignKey, Enum, DateTime, Integer, String, text
from sqlalchemy.orm import relationship
from pyramid.security import Allow

import base64
import os

from .meta import Base


def generate_token():
    return base64.urlsafe_b64encode(os.urandom(12)).decode("utf-8")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
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

    @property
    def organizations(self):
        result = []
        for has_organization in self.has_organizations:
            result.append(has_organization.organization)
        return result

    @property
    def root_organizations(self):
        result = []
        for has_organization in self.has_organizations:
            if has_organization.organization.parent_organization_id is None:
                result.append(has_organization.organization)
        return result

    def ensure_token_exists(self):
        if not self.auth_token:
            self.auth_token = generate_token()

    @property
    def display_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.first_name or self.last_name or self.email
