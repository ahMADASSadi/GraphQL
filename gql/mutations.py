from graphene.types import ObjectType

from gql.job.mutations import CreateJob, UpdateJob, DeleteJob
from gql.employer.mutations import CreateEmployer, UpdateEmployer, DeleteEmployer
from gql.user.mutations import LoginUser


class Mutation(ObjectType):
    create_job = CreateJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()

    create_employer = CreateEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()

    login_user = LoginUser.Field()
