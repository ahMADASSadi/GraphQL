# # # from graphene import Schema, ObjectType, String
# # # from fastapi import FastAPI
# # # import uvicorn
# # # from starlette.middleware.cors import CORSMiddleware
# # # from starlette_graphene3 import GraphQLApp, make_graphiql_handler

# # # app = FastAPI(title="GraphQL API")

# # # # Allow CORS (optional, but helps with frontend integration)
# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["*"],  # Change this to specific origins in production
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )

# # # # Define the GraphQL schema
# # # class Query(ObjectType):
# # #     hello = String(name=String(default_value="WORLD"))

# # #     def resolve_hello(self, info, name):
# # #         return f"Hello {name}"

# # # schema = Schema(query=Query)

# # # # Mount GraphQL endpoint with WebSocket support
# # # app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))

# # # if __name__ == "__main__":
# # #     uvicorn.run(app, host="127.0.0.1", port=8000, ws="websockets")

# # from fastapi import FastAPI
# # from ariadne.asgi import GraphQL
# # from ariadne import QueryType, make_executable_schema

# # app = FastAPI(title="GraphQL API")

# # # Define schema and resolvers
# # query = QueryType()

# # @query.field("hello")
# # def resolve_hello(_, info, name="WORLD"):
# #     """Returns a greeting message"""
# #     return f"Hello {name}"

# # type_defs = """
# #     type Query {
# #         "Returns a greeting message"
# #         hello(name: String = "WORLD"): String
# #     }
# # """

# # schema = make_executable_schema(type_defs, query)

# # # Mount GraphQL with Playground enabled
# # app.add_route("/graphql", GraphQL(schema, debug=True))

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="127.0.0.1", port=8000)

# from graphene import ObjectType, String, Schema, Int, Field, List, Mutation


# users = [
#     {"id": 1, "name": "John Doe", "age": "30", "sex": "Male"},
#     {"id": 2, "name": "Jane Doe", "age": "28", "sex": "Female"},
#     {"id": 3, "name": "Mike Doe", "age": "35", "sex": "Male"},
#     {"id": 4, "name": "Emily Doe", "age": "25", "sex": "Female"}
# ]


# class UserType(ObjectType):
#     id = Int()
#     name = String()
#     age = String()
#     sex = String()


# class CreateUser(Mutation):
#     class Arguments:
#         name = String()
#         age = String()
#         sex = String()

#     user = Field(UserType)

#     @staticmethod
#     def mutate(root, info, name, age, sex):
#         user = {"id": len(users) + 1, "name": name, "age": age, "sex": sex}
#         users.append(user)
#         return CreateUser(user=user)


# class UpdateUser(Mutation):
#     class Arguments:
#         id = Int(required=True)
#         name = String()
#         age = String()
#         sex = String()

#     user = Field(UserType)

#     @staticmethod
#     def mutate(root, info, id, name=None, age=None, sex=None):
#         user = [user for user in users if user["id"] == id]
#         if user:
#             user[0]["name"] = name if name else user[0]["name"]
#             user[0]["age"] = age if age else user[0]["age"]
#             user[0]["sex"] = sex if sex else user[0]["sex"]
#             return UpdateUser(user=user[0])
#         return UpdateUser(user=None)


# class DeleteUser(Mutation):
#     class Arguments:
#         id = Int(required=True)

#     user = Field(UserType)

#     @staticmethod
#     def mutate(root, info, id):
#         user_to_delete = None

#         # Find the user and delete
#         for idx, user in enumerate(users):
#             if user["id"] == id:
#                 user_to_delete = users.pop(idx)  # safely remove the user
#                 break

#         if user_to_delete:
#             # After deletion, adjust IDs for all subsequent users
#             for user in users:
#                 if user["id"] > id:
#                     user["id"] -= 1

#         return DeleteUser(user=user_to_delete)


# class Query(ObjectType):

#     user = Field(UserType, user_id=Int())

#     users_by_min_age = List(UserType, age=String())

#     @staticmethod
#     def resolve_user(root, info, user_id):
#         matched_user = [user for user in users if user["id"] == user_id]
#         return matched_user[0] if matched_user else None

#     @staticmethod
#     def resolve_users_by_min_age(root, info, age):
#         matched_users = [user for user in users if user["age"] >= str(age)]
#         return matched_users


# class Mutation(ObjectType):
#     create_user = CreateUser.Field()

#     update_user = UpdateUser.Field()

#     delete_user = DeleteUser.Field()


# schema = Schema(query=Query, mutation=Mutation)

# # query = """
# # mutation {
# #     createUser(name:"lawen",age:"23",sex:"female"){
# #         user{
# #             id
# #             name
# #             age
# #             sex
# #         }
# #     }
# # }
# # """

# update_query = """
# mutation {
#     updateUser(id:3 ,name:"lawen",age:"23",sex:"female"){
#         user{
#             id
#             name
#             age
#             sex
#         }
#     }
# }
# """

# delete_query = """
# mutation {
#     deleteUser(id:1){
#         user{
#         id
#         name 
#         age
#         sex }
#     }
# }
# """


# list_query = """
# query {
#     usersByMinAge(age: "23"){
#         id
#         name
#         age
#         sex
#     }
# }
# """

# user_query = """
# query {
#     user(userId: 3){
#         id
#         name
#         age
#         sex
#     }
# }
# """
# if __name__ == '__main__':

#     delete_result = schema.execute(delete_query)
#     print(delete_result)
#     print(users)
