from graphene.types import Mutation, String, Field

from gql.types import UserObject
from gql.user.utils import generate_token, get_authenticated_user,admin_user
from db.database import Session
from db.user.models import User
from datetime import datetime, timezone

from graphql import GraphQLError


class CreateAdminUser(Mutation):
    class Arguments:
        email = String(required=True)
        username = String(required=True)
        password_hash = String(required=True)
        role = String(required=True)

    user = Field(UserObject)

    @admin_user
    def mutate(root, info, email, username, password_hash, role):
        try:
            with Session() as session:
                try:
                    if session.query(User).filter_by(email=email).first():
                        raise GraphQLError("User already exists")
                    joined_at = datetime.now(timezone.utc)

                    user = User(email=email, username=username, role=role,
                                joined_at=joined_at)
                    user.set_password(password_hash)
                    session.add(user)
                    session.commit()
                    session.refresh(user)
                    return CreateAdminUser(user=user)
                except Exception as e:
                    session.rollback()
                    raise GraphQLError(f"Failed to create user: {str(e)}")
        except Exception as e:
            raise GraphQLError(f"An error occurred: {str(e)}")


class CreateUser(Mutation):
    class Arguments:
        email = String(required=True)
        username = String(required=True)
        password_hash = String(required=True)
    user = Field(UserObject)

    @staticmethod
    def mutate(root, info, email, username, password_hash):
        with Session() as session:
            try:
                if session.query(User).filter_by(email=email).first():
                    raise GraphQLError("User already exists")
                joined_at = datetime.now(timezone.utc)

                user = User(email=email, username=username,
                            joined_at=joined_at)
                user.set_password(password_hash)
                session.add(user)
                session.commit()
                session.refresh(user)
                return CreateUser(user=user)
            except Exception as e:
                session.rollback()
                raise GraphQLError(f"Failed to create user: {str(e)}")


class LoginUser(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)

    user = Field(UserObject)
    token = String()

    @staticmethod
    def mutate(self, info, email, password):
        with Session() as session:
            user = session.query(User).filter_by(email=email).first()
            if user and user.verify_password(password):
                token = generate_token(user.email)
                user.set_login_date(datetime.now(timezone.utc))
                session.commit()
                session.refresh(user)
                return LoginUser(user=user, token=token)
            return String("Invalid email or password")
