#!/usr/bin/env python3
"""Module for basic Auth
"""

from api.v1.auth.auth import Auth
import base64
from models.base import Base
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ Define Basic Auth class
    """
    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """ returns the Base64 part of the Authorization header for
        a Basic Authentication"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """returns the decoded value of a Base64 string
        base64_authorization_header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
        except (base64.binascii.Error, UnicodeDecodeError):
            return None
        return decoded.decode('utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """returns the user email and password
        from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        return (decoded_base64_authorization_header.split(":", 2)[0],
                decoded_base64_authorization_header.split(":", 2)[1])

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """ that returns the User instance based on his email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_email, str):
            return None
        base = User()
        search = base.search({"email": user_email})
        if len(search) == 0:
            return None
        user = search[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user
