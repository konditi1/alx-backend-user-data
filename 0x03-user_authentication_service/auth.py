#!/usr/bin/env python3
"""
hash_password
"""
import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register user
        Args:
            email (str): email
            password (str): password
        """
        user = self._db.find_user_by(email=email)
        if user:
            raise ValueError("User {} already exists".format(email))
        try:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        except ValueError:
            raise ValueError("User <user's email> already exists")


def valid_login(self, email: str, password: str) -> bool:
    """Validates user login credentials.

    Args:
        email (str): User's email.
        password (str): User's password.

    Returns:
        bool: True if login is successful, False otherwise.
    """
    user = self._db.find_user_by(email=email)
    if user and bcrypt.checkpw(
            password.encode('utf-8'), user.hashed_password):
        return True
    return False


def _hash_password(password: str) -> bytes:
    """Hashes the input password using bcrypt."""
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
