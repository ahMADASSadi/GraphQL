from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler
from graphene import String, ObjectType, Int, Schema, List, Field
from fastapi import FastAPI


from objects import jobs_data, employers_data


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employer(root, info):
        return next((employer for employer in employers_data if employer["id"] == root["employer_id"]))


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        return [job for job in jobs_data if job["employer_id"] == root["id"]]


class Query(ObjectType):

    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(root, info):
        return jobs_data

    @staticmethod
    def resolve_employers(root, info):
        return employers_data


schema = Schema(query=Query)


app = FastAPI(title="test")

app.mount("/graphql", GraphQLApp(schema=schema,
          on_get=make_playground_handler()))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
