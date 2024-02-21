#!/usr/bin/env python3
"""Auth module
"""
from typing import Union
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid


def _hash_password(password: str) -> bytes:
    """ hash password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """returns new new UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register new user"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        hashed_pass = _hash_password(password)
        return self._db.add_user(email, hashed_pass)

    def valid_login(self, email: str, password: str) -> bool:
        """ check if login valid"""
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """ creates session"""
        try:
            user = self._db.find_user_by(email=email)
            uuid = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=uuid)
        except (NoResultFound, InvalidRequestError, ValueError):
            return None
        return uuid

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ returns the corresponding User or None """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: int) -> None:
        """ destroys session"""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user_id=user.id, session_id=None)
        except (NoResultFound, InvalidRequestError, ValueError):
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ generet reset token"""
        try:
            user = self._db.find_user_by(email=email)
            uuid = _generate_uuid()
            self._db.update_user(user_id=user.id, reset_token=uuid)
        except (NoResultFound, InvalidRequestError, ValueError):
            raise ValueError
        return uuid

    def update_password(self, reset_token: str, password: str) -> None:
        """ reset password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        hashed_pass = _hash_password(password)
        self._db.update_user(user_id=user.id, hashed_password=hashed_pass)
        self._db.update_user(user_id=user.id, reset_token=None)
