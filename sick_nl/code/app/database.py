from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Based on tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:s0ps0ps0p@localhost:5432/feedback_database"
#SQLALCHEMY_DATABASE_URL = "postgresql://myuser:s0ps0ps0p@host.docker.internal:5432/feedback_database"
#SQLALCHEMY_DATABASE_URL = "postgresql://myuser:s0ps0ps0p@localhost:5432/feedback_database"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
