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
        return False
    
    def authorization_header(self, request=None) -> str:
        """ def Authorization header
        """
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """ get current user
        """
        return None
