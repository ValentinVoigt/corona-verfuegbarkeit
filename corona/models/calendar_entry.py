from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import relationship, backref
from pyramid.security import Allow

from .meta import Base


class CalendarEntry(Base):

    __tablename__ = "calendar_entry"

    id = Column(Integer, primary_key=True)
    organization_has_user_id = Column(ForeignKey("organizations_has_users.id"))
    calendar_entry_status_id = Column(ForeignKey("status.id"))
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    last_modified = Column(DateTime)
    start = Column(Date, nullable=False)
    end = Column(Date, nullable=False)

    status = relationship("Status")
    organization_has_user = relationship(
        "OrganizationHasUser",
        backref=backref("calendar", order_by="CalendarEntry.start"),
    )

    @classmethod
    def _factory(cls, request):
        return (
            request.dbsession.query(cls)
            .filter(cls.id == request.matchdict.get("id"))
            .one()
        )

    def __acl__(self):
        return [(Allow, f"user:{self.organization_has_user.user.id}", "edit")]
