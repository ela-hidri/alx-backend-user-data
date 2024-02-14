#!/usr/bin/env python3
"""Module for Auth
"""
from typing import List, TypeVar
import os


class Auth:
    """ define Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Define which routes don't need authentication
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths:
            return False
        if path[-1] != "/" and f'{path}/' in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ def Authorization header
        """
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ get current user
        """
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None
        return request.cookies.get(os.getenv('SESSION_NAME'))
