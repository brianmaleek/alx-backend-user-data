#!/usr/bin/env python3
"""
Module of SessionAuth class
"""


from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    SessionAuth class for session-based authentication.

    This class provides functionality for managing session IDs and user IDs
    associated with them.

    Attributes:
        user_id_by_session_id (dict): A class attribute to store user_id
            by session_id.
    """
    # Class attribute to store user_id by session_id
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a Session ID for a user_id.

        Args:
            user_id (str): The user ID for which the session ID is
                being created.

        Returns:
            str: The generated session ID if successful, otherwise None.
        """
        if user_id is None or type(user_id) is not str:
            return None
        # Generate Session ID using uuid module
        session_id = str(uuid.uuid4())
        # Store user_id by session_id
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Get the user ID associated with a session ID.

        Args:
            session_id (str): The session ID for which the user ID is
                being retrieved.

        Returns:
            str: The user ID if session ID exists, otherwise None.
        """
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieve the current user based on the session cookie.

        Args:
            request (flask.Request, optional): The Flask request object.
                Defaults to None.

        Returns:
            User: The current user instance if found, otherwise None.
        """
        if request is None:
            return None

        session_cookie = self.session_cookie(request)
        if session_cookie:
            user_id = self.user_id_for_session_id(session_cookie)
            if user_id:
                # Return the User instance based on user_id
                return User.get(user_id)

        return None
