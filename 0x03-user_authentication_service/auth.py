#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from db import DB
from user import User, Base
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
    Hashes the input password using bcrypt with salt.

    Args:
        password (str): The password string to be hashed.

    Returns:
        bytes: The salted hash of the input password.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    Generate a new UUID and return its string representation.

    Returns:
        str: String representation of the generated UUID.
    """
    return str(uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initialize a new Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with the given email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly registered User object.

        Raises:
            ValueError: If a given email of a user already exists.
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login information.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the user's information is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Create a new session for the user with the given email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID generated for the user.

        Raises:
            NoResultFound: If no user is found with the provided email.
            Return None if the email does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """Get the user corresponding to the given session ID.

        Args:
            session_id (str): The session ID of the user.

        Returns:
            User or None: The corresponding user if found, otherwise None.
        """
        if session_id is None:
            return None
        try:
            # Find the user by the session ID
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            # If no user found, return None
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session of the user with the given user ID.

        Args:
            user_id (int): The ID of the user.
        """
        self._db.update_user(user_id, session_id=None)
