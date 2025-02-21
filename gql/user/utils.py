from functools import wraps
import jwt
from datetime import datetime, timedelta, timezone
from db.user.models import User

from graphql import GraphQLError


from db.database import Session

SECRETE_KEY = "SOME_SECRETE_KEY"
ALGORITHM = "HS256"


def generate_token(email):
    exp_date = datetime.now(timezone.utc) + timedelta(days=1)
    payload = {
        "email": email,
        "exp": exp_date  # Convert to seconds since epoch
    }
    return jwt.encode(payload, SECRETE_KEY, algorithm=ALGORITHM)


def get_authenticated_user(context):
    request = context.get("request")
    header = request.headers.get("Authorization")
    if header and header.startswith("Bearer "):
        token = header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])

            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload["exp"], tz=timezone.utc):
                raise GraphQLError("Token has expired")
            with Session() as session:
                user = session.query(User).filter(
                    User.email == payload["email"]).first()
                if not user:
                    raise GraphQLError("Authentication failed")
                return user
        except jwt.InvalidTokenError:
            raise GraphQLError("Invalid token")
        except Exception as e:
            raise GraphQLError(f"An error occurred: {str(e)}")
    else:
        raise GraphQLError("Authentication required")

def get_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)
        return func(*args, user=user, **kwargs)
    return wrapper

def admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)
        if user.role != "admin":
            raise GraphQLError("Permission denied")
        return func(*args, **kwargs)
    return wrapper
