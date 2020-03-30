from sqlalchemy import Column, DateTime, ForeignKey, Float, Integer, String, text
from sqlalchemy.orm import relationship
from pyramid.security import Allow

from .meta import Base


permission_map = {
    "owner": 0,
    "admin": 1,
    "auditor": 2,
    "member": 3,
}


def permission_match(to_be_checked, minimum):
    return permission_map[to_be_checked] <= permission_map[minimum]


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
        return (
            [
                # Die Admins dieser Org oder darüber dürfen mich bearbeiten
                (Allow, f"user:{user.id}", "edit")
                for user in self.users_with_up("admin")
            ]
            + [
                (Allow, f"user:{user.id}", "details")
                for user in self.users_with_up("admin")
            ]
            + [
                (Allow, f"user:{user.id}", "view")
                for user in self.users_with_up("admin")
            ]
            + [
                # Die Auditoren dieser Org oder darüber dürfen meine Details einsehen
                (Allow, f"user:{user.id}", "details")
                for user in self.users_with_up("auditor")
            ]
            + [
                (Allow, f"user:{user.id}", "view")
                for user in self.users_with_up("auditor")
            ]
            + [
                # Alle Benutzer dieser Org oder darunter dürfen mich sehen
                # (damit man seinen eigenen Baum nach oben hin sehen kann)
                (Allow, f"user:{user.id}", "view")
                for user in self.users_with_down("member")
            ]
        )

    @property
    def recursive_users_up(self):
        return [h.user for h in self.recursive_has_users_up]

    @property
    def recursive_has_users_up(self):
        users = [h for h in self.has_users]
        if self.parent:
            users.extend(self.parent.recursive_has_users_up)
        return users

    @property
    def recursive_users_down(self):
        return [h.user for h in self.recursive_has_users_down]

    @property
    def recursive_has_users_down(self):
        users = [h for h in self.has_users]
        for child in self.children:
            users.extend(child.recursive_has_users_down)
        return users

    def users_with_up(self, permission):
        return [
            h.user
            for h in filter(
                lambda h: permission_match(h.permission, permission),
                self.recursive_has_users_up,
            )
        ]

    def users_with_down(self, permission):
        return [
            h.user
            for h in filter(
                lambda h: permission_match(h.permission, permission),
                self.recursive_has_users_down,
            )
        ]

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

    def num_available(self, day, day_or_night):
        """
        day_or_night: "day" oder "night"
        """
        result = 0
        for has_user in self.has_users:
            status = has_user.status_for(day)
            if status:
                result += 1 if status.is_available(day, day_or_night) else 0
        return result
