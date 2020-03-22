from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, text
from sqlalchemy.orm import relationship

from .meta import Base


class OrganizationHasUser(Base):
    __tablename__ = "organizations_has_users"

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey("organizations.id"))
    user_id = Column(ForeignKey("users.id"))
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    permission = Column(Enum("owner", "admin", "auditor", "member", name="permssions"))

    organization = relationship("Organization")
    user = relationship("User")
