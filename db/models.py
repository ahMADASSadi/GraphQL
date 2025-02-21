from db.user.models import User
from db.job.models import Job, JobApplication
from db.employer.models import Employer
from sqlalchemy import String, Integer, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from pathlib import Path
from sqlalchemy.orm import  sessionmaker
from passlib.hash import bcrypt

BASE_DIR = Path(__file__).parent.parent

load_dotenv(BASE_DIR)

DATABASE_URL = os.getenv("DB_URL")
engine = create_engine(DATABASE_URL, echo=True)
connection = engine.connect()
Session = sessionmaker(bind=engine)
