#!/usr/bin/env python3
"""
Module of SessionAuth class
"""


from api.v1.auth.auth import Auth
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
