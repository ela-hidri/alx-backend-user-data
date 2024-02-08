#!/usr/bin/env python3
"""
declarating filter_datum function
"""
import re

def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}', f'{field}={redaction}{separator}', message)
    return message
