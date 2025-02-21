from db.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Employer(Base):
    __tablename__ = 'employers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact_email = Column(String, nullable=False)
    industry = Column(String)
    jobs = relationship("Job", back_populates="employer", lazy='joined')
