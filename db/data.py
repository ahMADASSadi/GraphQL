import datetime
from passlib.hash import bcrypt

employers_data = [
    {"name": "MetaTechA",
        "contact_email": "contact@company-a.com", "industry": "Tech"},
    {"name": "MoneySoftB",
        "contact_email": "contact@company-b.com", "industry": "Finance"},
]

jobs_data = [
    {"title": "Software Engineer",
        "description": "Develop web applications", "employer_id": 1},
    {"title": "Data Analyst",
        "description": "Analyze data and create reports", "employer_id": 1},
    {"title": "Accountant",
        "description": "Manage financial records", "employer_id": 2},
    {"title": "Manager",
        "description": "Manage people who manage records", "employer_id": 2},
]

users_data = [
    {"username": "madassandd",
     "email": "madassandd@gmail.com",
     "role": "admin",
     "password_hash": f"{bcrypt.hash('13801121')}",
     "joined_at": datetime.datetime.now(),}
]

application_data =[
    {"user_id":1, "job_id":1},
]
