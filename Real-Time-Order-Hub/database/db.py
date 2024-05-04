# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import Session
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# url = os.getenv('DATABASE_URL')
# engine = create_engine(url)
# session = Session(engine)
#
# Base = declarative_base()
#
#
# def get_db():
#     try:
#         yield session
#         session.commit()
#     except:
#         raise
#     finally:
#         session.close()
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
# Define Base for SQLAlchemy ORM
Base = declarative_base()

# Load environment variables
load_dotenv()
url = os.getenv('DATABASE_URL')

# Create the SQLAlchemy engine
engine = create_engine(url)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a dependency that will provide a new SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

