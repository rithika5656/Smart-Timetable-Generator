"""
Smart Timetable Generator - Flask Web Application
"""
import logging
import time
from http import HTTPStatus
from typing import Tuple

from flask import Flask, render_template, request, Response
from timetable_generator import generate_timetable

# Import from new modules
from config import PORT, DEBUG, MAX_SUBJECTS, MAX_TEACHERS, MIN_PERIODS, MAX_PERIODS
from exceptions import TimetableError
from utils import api_response, extract_request_data, validate_request_data

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

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
        
    # Extract and Validate (using utils)
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
