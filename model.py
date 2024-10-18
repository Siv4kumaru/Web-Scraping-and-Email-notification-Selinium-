from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker,declarative_base

# Define the database URL
DATABASE_URL = 'sqlite:///example.db'

# Create an engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the User model
class Table(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Title= Column(Integer)
    Datetime = Column(String)
    Link = Column(String)
    Email_Sent = Column(Boolean)



    # Create the database and the table
    # Create a session (optional, can be used later for data manipulation)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Close the session
    session.close()

Base.metadata.create_all(engine)
