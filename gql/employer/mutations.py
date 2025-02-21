from graphene.types import Mutation, Field, String, Int, Boolean, List, NonNull
from graphql import GraphQLError

from db.employer.models import Employer
from db.job.models import Job
from db.database import Session

from gql.types import EmployerObject

from gql.user.utils import get_authenticated_user





class CreateEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)
        jobs = List(NonNull(Int), required=False)

    employer = Field(lambda: EmployerObject)

    authenticated_as = Field(String)

    @staticmethod
    def mutate(root, info, name, contact_email, industry, jobs=None):
        user = get_authenticated_user(info.context)
        with Session() as session:
            try:
                job_objects = session.query(Job).filter(
                    Job.id.in_(jobs)).all() if jobs else []

                employer = Employer(
                    name=name, contact_email=contact_email, industry=industry,
                    jobs=job_objects
                )

                session.add(employer)
                session.commit()
                session.refresh(employer)
                return CreateEmployer(employer=employer, authenticated_as=user.email)
            except Exception as e:
                session.rollback()  # Rollback the transaction on failure
                raise GraphQLError(f"Failed to create employer: {str(e)}")


class UpdateEmployer(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        contact_email = String()
        industry = Int()
        jobs = List(NonNull(Int))

    employer = Field(lambda: EmployerObject)

    @staticmethod
    def mutate(root, info, id, name=None, contact_email=None, industry=None, jobs=None):
        with Session() as session:
            try:

                employer = session.query(Employer).get(id)
                if name:
                    employer.name = name
                if contact_email:
                    employer.contact_email = contact_email
                if industry:
                    employer.industry = industry
                if jobs:
                    job_objects = session.query(Job).filter(
                        Job.id.in_(jobs)).all() if jobs else []

                    employer.jobs = job_objects
                session.add(employer)
                session.commit()
                session.refresh(employer)
                return UpdateEmployer(employer=employer)

            except Exception as e:
                session.rollback()
                raise GraphQLError(f"Failed to update employer: {str(e)}")


class DeleteEmployer(Mutation):
    class Arguments:
        id = Int(required=True)

    employer = Field(lambda: EmployerObject)
    success = Boolean()

    @staticmethod
    def mutate(root, info, id):
        with Session() as session:
            try:
                employer = session.query(Employer).get(id)
                session.delete(employer)
                session.commit()
                return DeleteEmployer(employer=employer, success=True)
            except Exception as e:
                raise Exception(f"Failed to delete employer: {str(e)}")
