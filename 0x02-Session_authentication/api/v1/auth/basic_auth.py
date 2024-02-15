#!/usr/bin/env python3
"""
BasicAuth that inherits from Auth
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User

import base64


class BasicAuth(Auth):
    """
    Basic Authentication manager for the API
    """
    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """
        Extracts the Base64 part of the Authorization header for
            Basic Authentication.

        Args:
            authorization_header (str): The Authorization header value.

        Returns:
            str: The Base64 part of the Authorization header.
        """
        if authorization_header is None or not isinstance(
                    authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
                self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 encoded value of a Base64 string.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str: The decoded value as UTF8 string.
        """
        if base64_authorization_header is None or not isinstance(
                    base64_authorization_header, str):
            return None

        try:
            decode_item = base64.b64decode(base64_authorization_header)
            decoded_str = decode_item.decode('utf-8')
            return decoded_str
        except Exception as e:
            return None

    def extract_user_credentials(
                self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the user credentials from a decoded Base64 string.

        Args:
            decoded_base64_authorization_header (str): The decoded
                Base64 string.

        Returns:
            (str, str): A tuple with the user email and password.
        """
        if decoded_base64_authorization_header is None or not isinstance(
                    decoded_base64_authorization_header, str) or \
                ':' not in decoded_base64_authorization_header:
            return (None, None)

        user_email, user_password = decoded_base64_authorization_header.\
            split(':', 1)
        return (user_email, user_password)

    def user_object_from_credentials(
                self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password.

        Args:
            user_email (str): The user email.
            user_pwd (str): The user password.

        Returns:
            TypeVar('User'): The User instance if the email and password
                are correct, None otherwise.
        """
        if user_email is None or not isinstance(user_email, str) or \
                user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception as e:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overloads Auth and retrieves the User instance for a request.

        Args:
            request (Request): The request to process.

        Returns:
            TypeVar('User'): The User instance if the request is
                authenticated
        """
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
