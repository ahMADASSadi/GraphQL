from db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class JobApplication(Base):
    __tablename__ = 'job_applications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    job = relationship("Job", back_populates="applications",
                       lazy='joined')  # Fixed naming
    user = relationship("User", back_populates="applications", lazy='joined')




class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="jobs", lazy='joined')
    applications = relationship(
        "JobApplication", back_populates="job", lazy='joined')  # Added back reference
