"""
Configuration settings for the application.
"""
import os

# Server Config
PORT: int = int(os.getenv("PORT", 5000))
DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
APP_VERSION: str = "1.0.0"

# Business Logic Constraints
DEFAULT_PERIODS: int = 6
MIN_PERIODS: int = 1
MAX_PERIODS: int = 10
MAX_SUBJECTS: int = 20
MAX_TEACHERS: int = 20

# Algorithm Config
START_HOUR: int = 9  # 9 AM
DEFAULT_DAYS: list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
BREAK_AFTER_PERIOD: int = 3  # Insert break after every 3 periods
ALLOWED_HOSTS: list = ["localhost", "127.0.0.1"]
SUPPORTED_LANGUAGES: list = ["en", "es", "fr"]

# Constraints Defaults
DEFAULT_MAX_CONSECUTIVE: int = 2
DEFAULT_MAX_DAILY: int = 4

# Security
API_KEY: str = os.getenv("API_KEY", "dev-api-key")
