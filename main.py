from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from graphene import Schema
from fastapi import FastAPI

from sqlalchemy import select
from gql.queries import Query
from gql.mutations import Mutation

from db.database import prepare_database, Session
from db.job.models import Job
from db.employer.models import Employer

schema = Schema(query=Query, mutation=Mutation)


app = FastAPI(title="Fast API", lifespan=prepare_database())


app.mount("/graphql", GraphQLApp(schema=schema,
          on_get=make_graphiql_handler()))


@app.get("/employers")
def get_employers():
    with Session() as session:
        return session.query(Employer).all()


@app.get("/jobs")
def get_jobs():
    with Session() as session:
        return session.query(Job).all()


@app.get("/jobs/{id}")
def get_job(id: int):
    with Session() as session:
        return session.query(Job).get(id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
