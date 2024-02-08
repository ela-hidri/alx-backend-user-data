#!/usr/bin/env python3
"""
declarating filter_datum function
"""
import re
from typing import List
import logging
PII_FIELDS = ['name', 'email', 'phone', 'ssn', 'password']


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """  filter values in incoming log records using filter_datum"""
        return filter_datum(self._fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """making logger """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.info)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(ch)
    return logger