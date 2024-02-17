#!/usr/bin/env python3
"""
Define a module that implements Session
Authentication with expiry date.
"""
from flask import request
from os import getenv
from datetime import (
        datetime,
        timedelta
        )

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    A session with an expiry date.
    """

    def __init__(self):
        """ Object constructor. """
        # Initialize session duration to 0 if
        # an invalid value is provided.
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a session for the given
        user. Store the session
        creation date as well.

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
        session_id = super().create_session(user_id)

        if (not session_id):
            return (None)

        self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
                }

        return (session_id)

    def user_id_for_session_id(self, session_id=None):
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
        # Abort method operation if no
        # session id is provided.
        if (not session_id):
            return (None)

        # Abort method operation if given
        # session id does not exist.
        if (session_id not in self.user_id_by_session_id):
            return (None)

        # Fetch the valid session details
        # containing the user id and
        # the created at attributes.
        session_data = self.user_id_by_session_id[session_id]

        # Fetch the id for the user
        # whose session duration is invalid.
        if (self.session_duration <= 0):
            return (session_data.get("user_id"))

        # Abort method operation if session
        # data doesn't contain created at
        # attribute.
        if (not session_data.get("created_at")):
            return (None)

        # Abort method operation if the
        # session is expired.
        # Session expiry date is from the
        # next session duration seconds after
        # the creation date.
        expire_date = session_data.get("created_at") +\
            timedelta(seconds=self.session_duration)

        from api.v1.app import app
        app.logger.error(expire_date)
        app.logger.error(datetime.now())
        app.logger.error(expire_date - datetime.now())

        if ((expire_date - datetime.now()).total_seconds() < 0):
            return (None)

        return (session_data.get("user_id"))