import os
import dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import event
from sqlalchemy import text
from sqlalchemy.engine import Engine
from contextvars import ContextVar

dotenv.load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'dbname')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

DATABASE_URL = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
    f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)

engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

current_schema = ContextVar("current_schema", default="public")

@event.listens_for(Engine, "connect")
def switch_schema(dbapi_connection, connection_record):
    schema = current_schema.get()
    cursor = dbapi_connection.cursor()
    cursor.execute(f'SET search_path TO {schema}')
    cursor.close()

def get_db():
    """ 
    Provides a database session for a single request.
    SessionLocal: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def set_tenant_schema(schema_name: str):
    """ 
    Sets the tenant schema for the current request.
    """
    current_schema.set(schema_name)

def create_schema(schema_name: str):
    """ 
    Creates a new schema in the database.
    """
    with engine.connect() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS {schema_name}'))
        connection.commit()
