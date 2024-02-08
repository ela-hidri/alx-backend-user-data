#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt

def hash_password(password: str) -> bytes[str]:
    """ hash password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())