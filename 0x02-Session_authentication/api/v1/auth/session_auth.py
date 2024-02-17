#!/usr/bin/env python3
"""
Define a module that implements Session
Authentication.
"""
from flask import request
from .auth import Auth
from uuid import uuid4

from models.user import User


class SessionAuth(Auth):
    """
    An instance of Session Authentication.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session for the given
        user.

        Parameters:
            user_id : str, optional
            The id for a user who needs
            a new session. Default value
            ensures method fails its
            operation.

        Return:
            A uuid4 string representing the
            session created. None is
            returned should the function
            fail its operation.
        """
        if (not user_id or not isinstance(user_id, str)):
            return (None)

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return (session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve the id for the user who
        owns the session with the given
        id.

        Parameters:
            session_id  : str, optional
            The id for the session whose
            user has to be retrieved. Default
            value ensures method fails its
            operation.

        Return:
            The id for the user with the
            given session. None is returned
            should the function fail its
            operation.
        """
        if (not session_id or not isinstance(session_id, str)):
            return (None)

        return (self.user_id_by_session_id.get(session_id))

    def current_user(self, request=None):
        """
        Obtain an instance for the current
        user.

        Parameters:
            request : LocalProxy
            A Flask request object to procss.

        Returns:
            An instance for the active user
            otherwise None.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        return (User.get(user_id))

    def destroy_session(self, request=None) -> bool:
        """
        Invalide the current session for the
        given request.

        Paameters:
            request : LocalProxy
            A Flask request object to process.

        Return:
            A boolean indicating whether the
            session is destroyed or nt.
        """
        if (not request):
            return (False)

        # Return false flag when the request
        # has no cookie (or the value None).
        session_id = self.session_cookie(request)
        if (not session_id):
            return (False)

        # Return false flag when session for
        # some reason is not for the current
        # user.
        if (not self.user_id_for_session_id(session_id)):
            return (False)

        # Delete user's session.
        del self.user_id_by_session_id[session_id]

        return (True)
