#!/usr/bin/env python3
"""
hash_password
"""
import bcrypt
from sqlalchemy.exc import NoResultFound

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
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))


def _hash_password(password: str) -> bytes:
    """Hash password
    Args:
        password (str): password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
