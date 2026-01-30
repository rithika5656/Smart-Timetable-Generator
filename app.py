"""
Smart Timetable Generator - Flask Web Application
"""
import os
import logging
import time
from http import HTTPStatus
from typing import Dict, List, Tuple, Any

from flask import Flask, render_template, request, jsonify, Response
from timetable_generator import generate_timetable

# --- Configuration ---
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Constants ---
DEFAULT_PERIODS = 6
MIN_PERIODS = 1
MAX_PERIODS = 10
MAX_SUBJECTS = 20
MAX_TEACHERS = 20

app = Flask(__name__)

# --- Custom Exceptions ---
class TimetableError(Exception):
    """Custom exception for timetable generation errors."""
    def __init__(self, message: str, status_code: int = HTTPStatus.BAD_REQUEST):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

# --- Helper Functions ---
def api_response(data: Any = None, error: str = None, status: int = 200) -> Tuple[Response, int]:
    """
    Helper to create a consistent JSON response.
    
    Args:
        data: The payload data (optional).
        error: Error message (optional).
        status: HTTP status code.
        
    Returns:
        Tuple containing the response object and status code.
    """
    payload = {}
    if data is not None:
        payload.update(data)
    if error is not None:
        payload["error"] = error
    return jsonify(payload), status

def extract_request_data(data: Dict[str, Any]) -> Tuple[List[str], List[str], int]:
    """
    Extract and clean data from the request.
    
    Args:
        data: The JSON request body.
        
    Returns:
        Tuple containing cleaned subjects, teachers, and periods.
    """
    subjects_raw = data.get("subjects", "")
    teachers_raw = data.get("teachers", "")
    periods_raw = data.get("periods_per_day", DEFAULT_PERIODS)
    
    # Clean strings and ensure uniqueness
    subjects = list(sorted(set([s.strip() for s in str(subjects_raw).split(",") if s.strip()])))
    teachers = list(sorted(set([t.strip() for t in str(teachers_raw).split(",") if t.strip()])))
    
    try:
        periods_per_day = int(periods_raw)
    except (ValueError, TypeError):
        raise TimetableError("Periods per day must be a valid integer")
        
    return subjects, teachers, periods_per_day

def validate_request_data(subjects: List[str], teachers: List[str], periods_per_day: int):
    """
    Validate the extracted data against business rules.
    
    Args:
        subjects: List of subjects.
        teachers: List of teachers.
        periods_per_day: Number of periods.
        
    Raises:
        TimetableError: If validation fails.
    """
    if not subjects:
        raise TimetableError("Please enter at least one subject")
    
    if not teachers:
        raise TimetableError("Please enter at least one teacher")
        
    if periods_per_day < MIN_PERIODS or periods_per_day > MAX_PERIODS:
        raise TimetableError(f"Periods per day must be between {MIN_PERIODS} and {MAX_PERIODS}")
        
    if len(subjects) > MAX_SUBJECTS:
        raise TimetableError(f"Too many subjects. Maximum allowed is {MAX_SUBJECTS}")
        
    if len(teachers) > MAX_TEACHERS:
        raise TimetableError(f"Too many teachers. Maximum allowed is {MAX_TEACHERS}")

# --- Error Handlers ---
@app.errorhandler(TimetableError)
def handle_timetable_error(error: TimetableError) -> Tuple[Response, int]:
    """Handle custom TimetableError exceptions."""
    logger.error(f"Timetable error: {error.message}")
    return api_response(error=error.message, status=error.status_code)

@app.errorhandler(Exception)
def handle_generic_error(error: Exception) -> Tuple[Response, int]:
    """Handle unexpected exceptions."""
    logger.exception("An unexpected error occurred")
    return api_response(error="An internal server error occurred", status=HTTPStatus.INTERNAL_SERVER_ERROR)

# --- Routes ---
@app.route("/health")
def health_check() -> Tuple[Response, int]:
    """
    Health check endpoint.
    
    Returns:
        JSON response indicating status.
    """
    return api_response(data={"status": "healthy", "timestamp": time.time()})

@app.route("/info")
def app_info() -> Tuple[Response, int]:
    """
    Application metadata endpoint.
    
    Returns:
        JSON response with app version and limits.
    """
    info = {
        "app": "Smart Timetable Generator",
        "version": "1.0.0",
        "limits": {
            "max_subjects": MAX_SUBJECTS,
            "max_teachers": MAX_TEACHERS,
            "periods_range": f"{MIN_PERIODS}-{MAX_PERIODS}"
        }
    }
    return api_response(data=info)

@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate() -> Tuple[Response, int]:
    """
    API endpoint to generate timetable.
    
    Returns:
        JSON response with the generated timetable.
    """
    logger.info("Received generation request")
    start_time = time.time()
    
    data = request.get_json()
    if not data:
        raise TimetableError("Invalid JSON body")
        
    # Extract and Validate
    subjects, teachers, periods_per_day = extract_request_data(data)
    validate_request_data(subjects, teachers, periods_per_day)
    
    # Generate
    try:
        result = generate_timetable(subjects, teachers, periods_per_day)
    except Exception as e:
        logger.error(f"Algorithm error: {str(e)}")
        raise TimetableError(f"Generation failed: {str(e)}", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    
    duration = time.time() - start_time
    logger.info(f"Timetable generated successfully in {duration:.4f}s")
    
    # Add metadata to result
    result["meta"] = {
        "generation_time_seconds": round(duration, 4),
        "status": "success"
    }
    
    return api_response(data=result)

if __name__ == "__main__":
    logger.info(f"Starting server on port {PORT}, debug={DEBUG}")
    app.run(debug=DEBUG, port=PORT)
