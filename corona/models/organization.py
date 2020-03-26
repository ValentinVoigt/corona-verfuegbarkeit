from sqlalchemy import Column, DateTime, ForeignKey, Float, Integer, String, text
from sqlalchemy.orm import relationship
from pyramid.security import Allow

from .meta import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    parent_organization_id = Column(ForeignKey("organizations.id"))
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    name = Column(String, nullable=False)
    city = Column(String)
    postal_code = Column(String)
    longitude = Column(Float(53))
    latitude = Column(Float(53))
    logo_url = Column(String)

    parent = relationship("Organization", backref="children", remote_side=[id])

    @classmethod
    def _factory(cls, request):
        return (
            request.dbsession.query(cls)
            .filter(cls.id == request.matchdict.get("id"))
            .one()
        )

    def __acl__(self):
        return [(Allow, f"user:{user.id}", "edit") for user in self.recursive_users]

    @property
    def recursive_users(self):
        users = [h.user for h in self.has_users]
        if self.parent:
            users.extend(self.parent.users)
        return users

    def has_user(self, email):
        return any([user.email.lower() == email.lower() for user in self.users])

    @property
    def recursive_roles(self):
        result = [(self, role) for role in self.roles]
        if self.parent:
            result.extend(self.parent.recursive_roles)
        return result

    @property
    def recursive_statuses(self):
        result = [(self, status) for status in self.statuses]
        if self.parent:
            result.extend(self.parent.recursive_statuses)
        return result

    @property
    def display_name(self):
        if self.parent:
            return f"{self.parent.name}, {self.name}"
        else:
            return self.name

    @property
    def uninvited_users(self):
        result = []
        for has_user in self.has_users:
            if not has_user.user.last_login and not has_user.user.last_invite:
                result.append(has_user.user)
        return result
