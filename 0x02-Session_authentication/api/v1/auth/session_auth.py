#!/usr/bin/env python3
"""Module for Auth
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ define SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        SessionId = str(uuid.uuid4())
        self.user_id_by_session_id[SessionId] = user_id
        return SessionId

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ that returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None
        return request.get('SESSION_NAME')
