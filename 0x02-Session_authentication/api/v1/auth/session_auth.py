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
            None
        if not isinstance(user_id, str):
            None
        SessionId = uuid.uuid4()
        self.user_id_by_session_id[SessionId] = user_id
        return SessionId
