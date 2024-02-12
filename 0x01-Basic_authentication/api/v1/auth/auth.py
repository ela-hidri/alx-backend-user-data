#!/usr/bin/env python3
"""Module for Auth
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ define Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ required auth
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
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ get current user
        """
        return None
