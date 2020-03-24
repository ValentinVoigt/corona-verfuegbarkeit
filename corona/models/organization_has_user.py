from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, text
from sqlalchemy.orm import relationship
from pyramid.security import Allow

from .meta import Base


class OrganizationHasUser(Base):
    __tablename__ = "organizations_has_users"

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey("organizations.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    permission = Column(
        Enum("owner", "admin", "auditor", "member", name="permssions"),
        nullable=False,
        default="member",
    )

    organization = relationship("Organization", backref="has_users")
    user = relationship("User", backref="has_organizations")

    @classmethod
    def _factory(cls, request):
        return (
            request.dbsession.query(cls)
            .filter(cls.id == request.matchdict.get("id"))
            .one()
        )

    def __acl__(self):
        return [(Allow, f"user:{user.id}", "edit") for user in self.organization.users]
