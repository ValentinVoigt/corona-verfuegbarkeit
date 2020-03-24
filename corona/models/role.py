from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from pyramid.security import Allow

from .meta import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey("organizations.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    minimum_required = Column(Integer)

    organization = relationship("Organization", backref="roles")

    @classmethod
    def _factory(cls, request):
        return (
            request.dbsession.query(cls)
            .filter(cls.id == request.matchdict.get("id"))
            .one()
        )

    def __acl__(self):
        return [(Allow, f"user:{user.id}", "edit") for user in self.organization.users]
