#!/usr/bin/env python3
"""DB module
"""
from typing import Type, Union

from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add user
                Args:
            email (str): email
            hashed_password (str): hashed password
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> Union[Type[User], None]:
        """Find user

        Args:
            **kwargs: arguments
        """
        if not kwargs:
            raise InvalidRequestError

        if len(kwargs) != 1:
            raise InvalidRequestError

        key, value = next(iter(kwargs.items()))

        if key not in ["id", "email", "session_id", "reset_token"]:
            raise InvalidRequestError

        try:
            if key == "id":
                return self._session.query(User).filter_by(id=value).one()
            elif key == "email":
                return self._session.query(User).filter_by(email=value).one()
            elif key == "session_id":
                return self._session.query(User).filter_by(
                    session_id=value).one()
            elif key == "reset_token":
                return self._session.query(User).filter_by(
                    reset_token=value).one()
        except NoResultFound:
            raise NoResultFound


if __name__ == "__main__":
    db = DB()
