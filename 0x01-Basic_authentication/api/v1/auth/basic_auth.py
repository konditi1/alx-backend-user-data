#!/usr/bin/env python3
"""class that ingerits from Auth"""
from base64 import b64decode, binascii
from typing import Tuple, Optional
from models.user import User
from .auth import Auth  # Assuming this is properly imported

class BasicAuth(Auth):
    def extract_base64_authorization_header(self, authorization_header: str) -> Optional[str]:
        """
       extract base64 authorization header to utf-8 string
        """
        prefix = "Basic "
        if not authorization_header or not isinstance(authorization_header, str) or not authorization_header.startswith(prefix):
            return None
        return authorization_header[len(prefix):]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> Optional[str]:
        """
        decode base64 authorization header to utf-8 string
        """
        if not base64_authorization_header or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = b64decode(base64_authorization_header, validate=True)
            return decoded_bytes.decode("utf-8")
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_auth_header: str) -> Tuple[Optional[str], Optional[str]]:
        if not decoded_base64_auth_header or not isinstance(decoded_base64_auth_header, str) or ':' not in decoded_base64_auth_header:
            return None, None
        return tuple(decoded_base64_auth_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> Optional[User]:
        if not all((user_email, user_pwd)) or not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if users:
                user = users[0]
                if user.is_valid_password(user_pwd):
                    return user
        except KeyError:
            pass
        return None

    def current_user(self, request=None) -> Optional[User]:
        auth_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(auth_header)
        decoded_auth_header = self.decode_base64_authorization_header(base64_auth_header)
        email, passwd = self.extract_user_credentials(decoded_auth_header)
        return self.user_object_from_credentials(email, passwd)
