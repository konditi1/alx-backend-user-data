#!/usr/bin/env python3
"""
Define a module that implements Basic
Authentication.
"""
from .auth import Auth
from base64 import b64decode, binascii
from typing import (
        Tuple,
        TypeVar
        )

from models.user import User


class BasicAuth(Auth):
    """
    An instance of Basic Authentication.
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """
        Extract the Base4 portion of the
        authorization header.

        Parameters:
            authorization_header : str
            A string containing the
            authorization for the current
            request. Obtained from the
            request header.

        Returns:
            The Base64 part of the authorization
            header.
        """
        prefix = "Basic "
        if (not authorization_header or
            not (isinstance(authorization_header, str)) or
                not authorization_header.startswith(prefix)):
            return (None)

        # Find the index of the next
        # character after the prefix
        start_index = (authorization_header.find(prefix) + 6)

        return (authorization_header[start_index:])

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        Returns the decoded value of a
        Base64 string from the authorization
        request header.

        Parameters:
            base64_authorization_header : str
            The Base64 part of the
            authorization header.

        Returns:
            The decode value of the Base64 part
            of the athorization header.
        """
        if (not base64_authorization_header or
                not isinstance(base64_authorization_header, str)):
            return (None)

        try:
            base_64_value = b64decode(base64_authorization_header,
                                      validate=True)

            return (base_64_value.decode("utf-8"))
        except (binascii.Error, UnicodeDecodeError):
            return (None)

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str]:
        """
        Extracts the username and passwords
        from the Base64 decoded value.

        Parameters:
            decoded_base64_authorization_header : str
            The decoded Base64 value.

        Returns:
            A tuple containing the email and
            password of the current user.
        """
        if (not decoded_base64_authorization_header or
            not isinstance(decoded_base64_authorization_header, str) or
                decoded_base64_authorization_header.find(":") == -1):
            return (None, None)

        return (tuple(decoded_base64_authorization_header.split(":", 1)))

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        Obtain the current user instance from
        the given credentials.

        Parameters:
            user_email : str
            The email for a user.

            user_pwd : str
            The password for a user.

        Returns:
            An instance of the `User` class
            representing an object for
            the current user.
        """
        if (not user_email or
                not isinstance(user_email, str)):
            return (None)

        if (not user_pwd or
                not isinstance(user_pwd, str)):
            return (None)

        list_of_users = []

        # Check to make sure DATA contains an
        # instance of the calling class
        try:
            list_of_users = User.search({"email": user_email})
        except KeyError:
            return (None)

        user = None

        # Check for an existing user
        if (len(list_of_users) == 0):
            return (None)

        # Check for valid user passwords
        user = list_of_users[0]
        if (not user.is_valid_password(user_pwd)):
            return (None)

        return (user)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user instance
        for the given request

        Parameters
            request : LocalProxy
            A Flask request object to process.

        Return:
            The user instance bearing the
            given request.
        """
        auth = self.authorization_header(request)
        auth_as_base_64 = self.extract_base64_authorization_header(auth)
        decoded_auth = self.decode_base64_authorization_header(auth_as_base_64)
        email, passwd = self.extract_user_credentials(decoded_auth)
        user = self.user_object_from_credentials(email, passwd)

        return (user)
