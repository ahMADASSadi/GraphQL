from graphene.types import Int, String, List, ObjectType, Field



class EmployerObject(ObjectType):
    id = Int()
    name = String()
    industry = String()
    contact_email = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        return root.jobs



class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)
    application = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_employer(root, info):
        return root.employer

    @staticmethod
    def resolve_application(root, info):
        return root.applications


class JobApplicationObject(ObjectType):
    id = Int()
    user_id = Int()
    job_id = Int()
    user = Field(lambda: UserObject)
    job = Field(lambda: JobObject)

    @staticmethod
    def resolve_user(root, info):
        return root.user

    @staticmethod
    def resolve_job(root, info):
        return root.job



class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    role = String()
    password = String()
    application = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_users(root, info):
        return root.users

    @staticmethod
    def resolve_application(root, info):
        return root.applications
