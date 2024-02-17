#!/usr/bin/env python3
""" Module of Auth
"""
from api.v1.views import app_views
from flask import request
from models.user import User
from os import getenv
from typing import List, TypeVar


class Auth():
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: list = None) -> bool:
        """ Require auth
        """
        if excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> str:
        """ Current user
        """
        if request is None:
            return None

    def session_cookie(self, request=None) -> str:
        """ Session cookie
        """
        if (not request):
            return (None)

        return (request.cookies.get(getenv("SESSION_NAME")))    
