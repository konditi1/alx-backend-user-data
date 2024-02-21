#!/usr/bin/env python3
"""
hash_password
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash password
    Args:
        password (str): password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
