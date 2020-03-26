from sqlalchemy import Table, Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from pyramid.security import Allow

from .meta import Base

UserHasRole = Table(
    "users_has_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True, nullable=False,),
    Column("role_id", ForeignKey("roles.id"), primary_key=True, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=text("now()")),
)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey("organizations.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    minimum_required = Column(Integer)

    organization = relationship("Organization", backref="roles")
    users = relationship("User", secondary=UserHasRole, backref="roles")

    @classmethod
    def _factory(cls, request):
        return (
            request.dbsession.query(cls)
            .filter(cls.id == request.matchdict.get("id"))
            .one()
        )

    def __acl__(self):
        return [
            (Allow, f"user:{user.id}", "edit")
            for user in self.organization.users_with_up("admin")
        ]
