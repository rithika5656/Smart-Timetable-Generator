"""
Custom exceptions for the application.
"""
from http import HTTPStatus

class TimetableError(Exception):
    """Custom exception for timetable generation errors."""
    def __init__(self, message: str, status_code: int = HTTPStatus.BAD_REQUEST):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
