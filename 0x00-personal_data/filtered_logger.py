#!/usr/bin/env python3
"""
0x00. Personal data
"""

import re
import logging
from typing import List


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
