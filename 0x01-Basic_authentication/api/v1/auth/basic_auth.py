#!/usr/bin/env python3
"""Module for basic Auth
"""

from api.v1.auth.auth import Auth
import base64

class BasicAuth(Auth):
    """ Define Basic Auth class
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization header for 
        a Basic Authentication"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return base64.b64encode(authorization_header)
