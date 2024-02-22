#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

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
        """Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created User object.
        """
        if not email or not hashed_password:
            return
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database based on input arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering the query.

        Returns:
            User: The first user found matching the query.

        Raises:
            NoResultFound: If no user is found matching the query.
            InvalidRequestError: If invalid query arguments are passed.
        """
        if not kwargs:
            raise InvalidRequestError

        find_user = self._session.query(User).filter_by(**kwargs).one()
        if not find_user:
            raise NoResultFound
        return find_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes based on user_id.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments containing user attributes
            to update.

        Raises:
            ValueError: If an invalid argument is passed.
            NoResultFound: If the user with the given user_id is not found.
        """
        if not user_id or not kwargs:
            return None
        user_to_update = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user_to_update, key):
                raise ValueError
            setattr(user_to_update, key, value)
        self._session.commit()
