#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from db import DB
from user import User, Base
from sqlalchemy.orm.exc import NoResultFound


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
