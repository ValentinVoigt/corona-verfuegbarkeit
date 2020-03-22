from sqlalchemy import Column, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship

from .meta import Base


class OrganizationHasUserHasRole(Base):
    __tablename__ = "organizations_has_users_has_roles"

    organizations_has_users = Column(
        ForeignKey("organizations_has_users.id"), primary_key=True, nullable=False
    )
    role_id = Column(ForeignKey("roles.id"), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))

    organizations_has_user = relationship("OrganizationHasUser")
    role = relationship("Role")
