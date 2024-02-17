#!/usr/bin/env python3
"""
Define a module that implements Session Authentication with expiry date.
"""

from flask import request
from os import getenv
from datetime import datetime, timedelta
from .session_auth import SessionAuth

class SessionExpAuth(SessionAuth):
    """
    A session with an expiry date.
    """

    def __init__(self):
        """
        Initialize the SessionExpAuth object.
        """
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a session for the given user and store the creation date.

        Parameters:
            user_id (str): The id for a user who needs a new session.

        Returns:
            str: A uuid4 string representing the created session, or None if the operation fails.
        """
        session_id = super().create_session(user_id)

        if not session_id:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the id for the user who owns the session with the given id.

        Parameters:
            session_id (str): The id for the session whose user needs to be retrieved.

        Returns:
            str: The id for the user with the given session, or None if the operation fails.
        """
        if not session_id:
            return None

        if session_id not in self.user_id_by_session_id:
            return None

        session_data = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_data.get("user_id")

        if not session_data.get("created_at"):
            return None

        expire_date = session_data.get("created_at") + timedelta(seconds=self.session_duration)

        from api.v1.app import app  # Consider importing app at the top level to avoid circular imports.
        app.logger.error(expire_date)
        app.logger.error(datetime.now())
        app.logger.error(expire_date - datetime.now())

        if (expire_date - datetime.now()).total_seconds() < 0:
            return None

        return session_data.get("user_id")
