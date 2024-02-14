#!/usr/bin/env python3
"""class that ingerits from Auth"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """inherits from Auth"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """returns Base64 part of the Authorization header"""
        if authorization_header is None or\
                not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        if authorization_header.find('Basic ') == -1:
            return None
        return authorization_header[authorization_header.find('Basic ')+6:]
    