from sqlalchemy import create_engine, Column, func, DateTime
from sqlalchemy.orm import declarative_base, Session, mapped_column, Mapped
from sqlalchemy.orm import sessionmaker

url = 'postgresql://postgres:postgres@localhost:5439/postgres'
engine = create_engine(url)
session = Session(engine)
Base = declarative_base()


def get_db():
    try:
        yield session
        session.commit()
    except Exception:
        raise
    finally:
        session.close()


# _id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]
class Data(Base):
    __tablename__ = 'data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time: Mapped[str] = Column(DateTime, default=func.utcnow)
    name: Mapped[str] = mapped_column(nullable=False)
    k_to_usd: Mapped[float] = mapped_column(nullable=False)

# Docker: 1ed6fa6ef3ee8fb1bd91524b38857389b32ba397b01e4bf92476ac8f270eb42a
