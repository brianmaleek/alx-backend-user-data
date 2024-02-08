#!/usr/bin/env python3
"""
0x00. Personal data
"""

import re
import logging
import mysql.connector
import os
from typing import List


"""
- Create a tuple PII_FIELDS constant at the root of the module containing the
    fields from user_data.csv that are considered PII.
- PII_FIELDS can only contain 5 fields - choose the right list of fields that
    are considered as “important” PIIs or information that you must hide in
    your logs. Use it to parameterize the formatter.
"""
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize RedactingFormatter with a list of fields to redact.

        Args:
        - fields (List[str]): A list of strings representing fields to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record.

        This method redacts specified fields in the log message.

        Args:
        record (logging.LogRecord): The log record to be formatted.

        Returns:
        str: The formatted log message.
        """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """
    - Obfuscates specified fields in a log message.

    Arguments:
        - fields: A list of strings representing the fields to obfuscate.
        - redaction: A string representing by what the field will be
                obfuscated.
        - message: A string representing the log line.
        - separator: A string representing by which character is separating
                all fields in the log line.

    Returns:
    - A string representing the log message with specified fields obfuscated.
    """
    for field in fields:
        message = re.sub(fr'{re.escape(field)}=.+?{re.escape(separator)}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    - Create a get_logger function that takes no arguments and returns a 
        logging.Logger object.
    - The logger should be named "user_data" and only log up to logging.INFO
        level. It should not propagate messages to other loggers. It should
        have a StreamHandler with RedactingFormatter as formatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    """
    return mysql.connector.connect(
        host="localhost
