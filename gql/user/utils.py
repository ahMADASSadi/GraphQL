import jwt
from datetime import datetime, timedelta, timezone
SECRETE_KEY = "SOME_SECRETE_KEY"
ALGORITHM = "HS256"


def generate_token(user_id, email, role):
    exp_date = datetime.now(timezone.utc) + timedelta(days=1)
    payload = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "exp": exp_date  # Convert to seconds since epoch
    }
    return jwt.encode(payload, SECRETE_KEY, algorithm=ALGORITHM)
