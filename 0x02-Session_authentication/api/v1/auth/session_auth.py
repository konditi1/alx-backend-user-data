#!/usr/bin/env python3
"""
Define a module that implements Session Authentication.
"""
from flask import request
from .auth import Auth
from uuid import uuid4

from models.user import User


class SessionAuth(Auth):
    """
    An instance of Session Authentication.

    Attributes:
        user_id_by_session_id (dict): A dictionary mapping session IDs to user IDs.

    Methods:
        create_session(user_id: str = None) -> str: Creates a session for the given user.
        user_id_for_session_id(session_id: str = None) -> str: Retrieves the user ID
        current_user(request=None): Obtains an instance for the current user.
        destroy_session(request=None) -> bool: Invalidates the current session for the given request.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session for the given user.

        Parameters:
            user_id (str): The ID of the user for whom a new session is created.

        Returns:
            str: A uuid4 string representing the created session. 
                 None is returned if the operation fails.
        """
        if not user_id or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve the user ID for the session with the given ID.

        Parameters:
            session_id (str): The ID of the session.

        Returns:
            str: The user ID associated with the session ID.
                 None is returned if the session ID is invalid or not found.
        """
        if not session_id or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Obtain an instance for the current user.

        Parameters:
            request: The Flask request object.

        Returns:
            User: An instance representing the current user.
                  None is returned if the session is not found or invalid.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Invalidate the current session for the given request.

        Parameters:
            request: The Flask request object.

        Returns:
            bool: True if the session is successfully destroyed, False otherwise.
        """
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        if not self.user_id_for_session_id(session_id):
            return False

        del self.user_id_by_session_id[session_id]

        return True
