"""
module to handle database connection
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.settings import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://myusername:mypassword@postgresql:5432/postgres'
SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{settings.database_username}:'
    f'{settings.database_password}@{settings.database_hostname}'
    f':{settings.database_port}/{settings.database_name}'
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
