#!/usr/bin/env python3
"""
encrypt_password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash password
    :param password:
    :return:
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    is_valid
    :param hashed_password:
    :param password:
    :return:
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
