#!/usr/bin/env python3
"""
Class manages the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Authentication manager for the API
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a given path.

        Args:
            - path (str): The path to be checked for authentication
                requirement.
            - excluded_paths (List[str]): A list of paths that are
                excluded from authentication.

        Returns:
            - bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path.rstrip("/") + "/"
        for p in excluded_paths:
            if p.endswith("*") and path.startswith(p[:-1]):
                return False
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.

        Args:
            - request (flask.Request, optional): The Flask request object
                Defaults to None.

        Returns:
            - str: The authorization header value.
        """
        if request is None:
            return None

        if "Authorization" not in request.headers:
            return None

        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Retrieves the current user from the request.

        Args:
            - request (flask.Request, optional): The Flask request object
                Defaults to None.

        Returns:
            - TypeVar('User'): The current user object.
        """
        return None
