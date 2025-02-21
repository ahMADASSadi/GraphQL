from db.base import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)  # Changed from `password`
    applications = relationship(
        "JobApplication", back_populates="user", lazy='joined')  # Added this line
    joined_at = Column(DateTime, nullable=False)
    last_login = Column(DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)
