from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import relationship

from .meta import Base


class CalendarEntry(Base):

    __tablename__ = "calendar_entry"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    calendar_entry_status_id = Column(ForeignKey("status.id"))
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    last_modified = Column(DateTime)
    start = Column(Date, nullable=False)
    end = Column(Date, nullable=False)

    calendar_entry_status = relationship("Status")
    user = relationship("User")
