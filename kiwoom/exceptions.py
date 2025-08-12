# -*- coding: utf-8 -*-
"""
kiwoom.exceptions
~~~~~~~~~~~~~~~~~

This module contains the set of Kiwoom's exceptions.
"""


class KiwoomException(Exception):
    """Base exception for all python-kiwoom errors."""


class KiwoomAPIError(KiwoomException):
    """Indicates an error from the Kiwoom API.

    Attributes:
        response: The HTTPX response object.
        error_code: The error code returned by the API.
        error_message: The error message returned by the API.
    """

    def __init__(self, response, error_code: str = None, error_message: str = None):
        self.response = response
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(f"[{self.error_code}] {self.error_message}")


class AuthenticationError(KiwoomException):
    """Indicates an authentication error."""


class WebSocketError(KiwoomException):
    """Indicates a WebSocket related error."""
