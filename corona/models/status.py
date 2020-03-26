from sqlalchemy import Column, DateTime, Boolean, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from pyramid.security import Allow

from .meta import Base


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey("organizations.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    color = Column(String, nullable=False)
    is_available = Column(Boolean, nullable=False)

    organization = relationship("Organization", backref="statuses")

    @classmethod
    def _factory(cls, request):
        return (
            request.dbsession.query(cls)
            .filter(cls.id == request.matchdict.get("id"))
            .one()
        )

    def __acl__(self):
        return [(Allow, f"user:{user.id}", "edit") for user in self.organization.users]
