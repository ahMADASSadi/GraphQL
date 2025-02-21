from db.models import Employer, Job, User, engine, Session, JobApplication
from db.data import jobs_data, employers_data, users_data, application_data
from db.base import Base

def prepare_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = Session()

    for employer in employers_data:
        session.add(Employer(**employer))

    for job in jobs_data:
        session.add(Job(**job))

    for user in users_data:
        session.add(User(**user))

    for application in application_data:
        session.add(JobApplication(**application))
        
    session.commit()
