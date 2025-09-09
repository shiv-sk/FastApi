from sqlmodel import create_engine, SQLModel, Session

db_url = "postgres_local_database_url"
engine = create_engine(db_url , echo=True)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session