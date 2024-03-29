#!/usr/bin/env python3
"""
declarating filter_datum function
"""
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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
    logger.propagate = False

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    logger.addHandler(ch)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a connector to database"""
    return mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )


def main() -> None:
    """retrieve all rows from db"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELCET * FROM FROM users;")
    logger = get_logger()
    headers = []
    for des in cursor.description:
        headers.append(des)
    for row in cursor:
        ans = ''
        for r, h in zip(row, headers):
            ans += f'{h}={r};'
        logger.info(ans)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
