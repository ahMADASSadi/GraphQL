from graphene.types import Mutation, String, Field

from gql.types import UserObject
from gql.user.utils import generate_token
from db.database import Session
from db.user.models import User

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
                token = generate_token(user.id, user.email, user.role)
                return LoginUser(user=user, token=token)
            return String("Invalid email or password")