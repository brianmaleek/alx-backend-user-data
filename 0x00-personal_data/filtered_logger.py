#!/usr/bin/env python3
"""
0x00. Personal data
"""

import re
from typing import List


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
