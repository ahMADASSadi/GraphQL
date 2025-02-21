from graphene.types import Mutation, Field, String, Int, Boolean
from graphql import GraphQLError

from db.job.models import Job, JobApplication
from db.database import Session

from gql.user.utils import get_user
from gql.types import JobObject, JobApplicationObject


class CreateJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, title, description, employer_id):
        with Session() as session:
            try:
                job = Job(title=title, description=description,
                          employer_id=employer_id)
                session.add(job)
                session.commit()
                session.refresh(job)
                return CreateJob(job=job)
            except Exception as e:
                return String(f"Failed to create job: {str(e)}")


class UpdateJob(Mutation):
    class Arguments:
        id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, id, title=None, description=None, employer_id=None):
        with Session() as session:
            try:
                job = session.query(Job).get(id)
                if job:
                    if title:
                        job.title = title
                    if description:
                        job.description = description
                    if employer_id:
                        job.employer_id = employer_id
                    session.commit()
                    session.refresh(job)
                    return UpdateJob(job=job)
            except Exception as e:
                raise Exception(f"Failed to update job: {str(e)}")


class DeleteJob(Mutation):
    class Arguments:
        id = Int(required=True)

    job = Field(lambda: JobObject)
    success = Boolean()

    @staticmethod
    def mutate(root, info, id):
        with Session() as session:
            try:
                job = session.query(Job).get(id)
                session.delete(job)
                session.commit()
                return DeleteJob(job=job, success=True)
            except Exception as e:
                raise Exception(f"Failed to delete job: {str(e)}")


class CreateJobApplication(Mutation):
    class Arguments:
        job_id = Int(required=True)
        # user_id = Int(required=True)

    job_application = Field(lambda: JobApplicationObject)
    success = Boolean()

    @get_user
    @staticmethod
    def mutate(root, info, job_id, user):
        with Session() as session:
            print(user.id)
            try:
                if session.query(JobApplication).filter(JobApplication.job_id == job_id, JobApplication.user_id == user.id).first():
                    raise GraphQLError("Job application already exists")
                job_application = JobApplication(
                    job_id=job_id, user_id=user.id)
                session.add(job_application)
                session.commit()
                session.refresh(job_application)
                return CreateJobApplication(job_application=job_application, success=True)
            except Exception as e:
                raise GraphQLError(
                    f"Failed to create job application: {str(e)}")
