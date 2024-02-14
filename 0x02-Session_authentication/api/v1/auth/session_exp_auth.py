#!/usr/bin/env python3
"""Module for SessionExpAuth routes
"""
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    """ define Session ExpAuth class"""
    def __init__(self):
        """ init """
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Overload create session"""
        sessionId = super().create_session(user_id)
        if sessionId is None:
            return None
        self.user_id_by_session_id["session dictionary"] = sessionId
        self.user_id_by_session_id['user_id'] = sessionId
        self.user_id_by_session_id['created_at'] = datetime.now()
        return sessionId

    def user_id_for_session_id(self, session_id=None):
        """ overload user_id_for_session_id """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id['user_id']
        if "created_at" not in self.user_id_by_session_id:
            return None
        startTime = self.user_id_by_session_id['created_at']
        session_duration = startTime + self.session_duration
        time_diff = datetime.now() - session_duration
        if time_diff < timedelta(0):
            return None
        return self.user_id_by_session_id['user_id']
