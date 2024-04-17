#!/usr/bin/python3
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base, BaseModel


class DBStorage:
    """Represents a db: The working SQLAlchemy session."""

    def __init__(self, user, pwd, host, db_name):
        """Initialize a new DBStorage instance."""

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{pwd}@{host}/{db_name}", pool_pre_ping=True
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def all(self, cls=None):
        """Query on the current database session all objects of the given class."""
        if cls is None:
            return {
                f"{type(o).__name__}.{o.id}": o
                for o in self.__session.query(Base)
            }
        else:
            if type(cls) == str:
                cls = eval(cls)
            return {f"{type(o).__name__}.{o.id}": o.as_dict() for o in self.__session.query(cls)}

    def new(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()
