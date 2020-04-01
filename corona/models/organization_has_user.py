from sqlalchemy import Table, Column, DateTime, Enum, ForeignKey, Integer, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from pyramid.security import Allow

from .meta import Base

OrganizationHasUserHasRole = Table(
    "organizations_has_users_has_roles",
    Base.metadata,
    Column(
        "organizations_has_users_id",
        ForeignKey("organizations_has_users.id"),
        primary_key=True,
        nullable=False,
    ),
    Column("role_id", ForeignKey("roles.id"), primary_key=True, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=text("now()")),
)


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
    roles = relationship(
        "Role", secondary=OrganizationHasUserHasRole, backref="has_users"
    )
    role_ids = association_proxy("roles", "id")

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
            for user in self.organization.recursive_users_up
        ] + [
            (Allow, f"user:{h.user.id}", "calendar")
            for h in self.organization.has_users
        ]

    def status_for(self, day):
        for entry in self.calendar:
            if entry.start <= day <= entry.end:
                return entry.status
