from graphene.types import Mutation,Field,String,Int,Boolean


from db.job.models import Job
from db.database import Session

from gql.types import JobObject

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
