from graphene.types import ObjectType

from gql.job.mutations import CreateJob, UpdateJob, DeleteJob, CreateJobApplication
from gql.employer.mutations import CreateEmployer, UpdateEmployer, DeleteEmployer
from gql.user.mutations import LoginUser, CreateUser, CreateAdminUser


class Mutation(ObjectType):
    create_job = CreateJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()

    create_job_application = CreateJobApplication.Field()

    create_employer = CreateEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()

    login_user = LoginUser.Field()
    create_user = CreateUser.Field()
    create_admin_user = CreateAdminUser.Field()
