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
