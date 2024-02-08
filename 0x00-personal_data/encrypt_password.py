#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt
from typing import ByteString


def hash_password(password: str) -> ByteString:
    """ hash password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
