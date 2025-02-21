from graphene.types import List, ObjectType, Mutation, String, Field, Int

from gql.types import UserObject
from db.user.models import User

from db.models import Session

from sqlalchemy.orm import joinedload

from gql.types import JobObject,JobApplicationObject
from db.job.models import Job,JobApplication
from db.employer.models import Employer
from gql.types import EmployerObject

class Query(ObjectType,
            ):
    users = List(UserObject)
    user = Field(UserObject, id=Int(required=True))

    @staticmethod
    def resolve_users(root, info):
        with Session() as session:
            return session.query(User).all()

    @staticmethod
    def resolve_user(root, info, id):
        with Session() as session:
            return session.query(User).get(id)

    jobs = List(JobObject)
    job = Field(JobObject, id=Int(required=True))
    job_applications = List(JobApplicationObject)

    @staticmethod
    def resolve_job_applications(root, info):
        with Session() as session:
            return session.query(JobApplication).all()

    @staticmethod
    def resolve_jobs(root, info):
        with Session() as session:
            # return session.query(Job).all()
            return session.query(Job).options(joinedload(Job.employer)).all()

    @staticmethod
    def resolve_job(root, info, id):
        with Session() as session:
            return session.query(Job).options(joinedload(Job.employer)).get(id)

    employers = List(EmployerObject)
    employer = Field(EmployerObject, id=Int(required=True))

    @staticmethod
    def resolve_employers(root, info):
        with Session() as session:
            return session.query(Employer).options(joinedload(Employer.jobs)).all()

    @staticmethod
    def resolve_employer(root, info, id):
        with Session() as session:
            return session.query(Employer).options(joinedload(Employer.jobs)).get(id)
