"""
Configuration settings for the application.
"""
import os

# Server Config
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
APP_VERSION = "1.0.0"

# Business Logic Constraints
DEFAULT_PERIODS = 6
MIN_PERIODS = 1
MAX_PERIODS = 10
MAX_SUBJECTS = 20
MAX_TEACHERS = 20

# Algorithm Config
START_HOUR = 9  # 9 AM
DEFAULT_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
BREAK_AFTER_PERIOD = 3  # Insert break after every 3 periods
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
SUPPORTED_LANGUAGES = ["en", "es", "fr"]
