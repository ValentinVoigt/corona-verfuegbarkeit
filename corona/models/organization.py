from sqlalchemy import Column, DateTime, ForeignKey, Float, Integer, String, text
from sqlalchemy.orm import relationship

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

    parent_organization = relationship("Organization", remote_side=[id])
