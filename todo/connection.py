from sqlmodel import create_engine
# postgresql_database_url
database_url = "localhost_postgres_url"
# connection establishment
engine = create_engine(database_url, echo=True)