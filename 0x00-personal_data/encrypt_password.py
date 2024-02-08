#!/usr/bin/env python3
""" Encrypting passwords """
import bcrypt


def hash_password(password: str) -> bytes:
    """
    - User passwords should NEVER be stored in plain text in a database.
    - Implement a hash_password function that expects one string argument name
        password and returns a salted, hashed password, which is a byte string.
    - Use the bcrypt package to perform the hashing (with hashpw).
    """

    encode = password.encode()
    hashed = bcrypt.hashpw(encode, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates whether the provided password matches the hashed password.

    Args:
    hashed_password (bytes): The salted, hashed password.
    password (str): The password to validate.

    Returns:
    bool: True if the password matches the hashed password, False otherwise.
    """
    valid = False
    encode = password.encode()
    if bcrypt.checkpw(encode, hashed_password):
        valid = True
    return valid
