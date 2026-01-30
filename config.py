"""
Configuration settings for the application.
"""
import os

# Server Config
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Business Logic Constraints
DEFAULT_PERIODS = 6
MIN_PERIODS = 1
MAX_PERIODS = 10
MAX_SUBJECTS = 20
MAX_TEACHERS = 20
