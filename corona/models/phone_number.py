from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from .meta import Base


class PhoneNumber(Base):
    __tablename__ = "phone_numbers"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    label = Column(String)
    phone_number = Column(String, nullable=False)

    user = relationship("User")
