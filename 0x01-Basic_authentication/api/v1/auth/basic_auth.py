#!/usr/bin/env python3
"""
BasicAuth that inherits from Auth
"""
from api.v1.auth.auth import Auth
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
