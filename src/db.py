from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:////data/db.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    v_token = Column(String, nullable=False)
    student_name = Column(String, nullable=False)

Base.metadata.create_all(engine)
