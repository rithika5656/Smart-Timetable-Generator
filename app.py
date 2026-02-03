"""
Smart Timetable Generator - Flask Web Application
"""
import logging
import time
from http import HTTPStatus
from typing import Tuple

from flask import Flask, render_template, request, Response, jsonify

from scheduler import generate_scheduler_response
from config import PORT, DEBUG, MAX_SUBJECTS, MAX_TEACHERS, MIN_PERIODS, MAX_PERIODS
from exceptions import TimetableError
from utils import api_response, extract_request_data, validate_request_data, generate_csv
from database import init_app, get_db

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

# --- Database Init ---
init_app(app)

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
    """Health check endpoint."""
    return api_response(data={"status": "healthy", "timestamp": time.time()})

@app.route("/info")
def app_info() -> Tuple[Response, int]:
    """Application metadata endpoint."""
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
    """API endpoint to generate timetable."""
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
        result = generate_scheduler_response(subjects, teachers, periods_per_day)
    except Exception as e:
        logger.error(f"Algorithm error: {str(e)}")
        raise TimetableError(f"Generation failed: {str(e)}", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    
    duration = time.time() - start_time
    logger.info(f"Timetable generated successfully in {duration:.4f}s")
    
    # Add metadata
    result["meta"] = {
        "generation_time_seconds": round(duration, 4),
        "status": "success"
    }
    
    # Save to History
    try:
        db = get_db()
        db.execute(
            'INSERT INTO history (subjects, teachers, periods, duration, status) VALUES (?, ?, ?, ?, ?)',
            (str(len(subjects)), str(len(teachers)), periods_per_day, duration, 'success')
        )
        db.commit()
    except Exception as e:
        logger.error(f"DB Error: {e}")

    return api_response(data=result)

@app.route("/validate", methods=["POST"])
def validate_input() -> Tuple[Response, int]:
    """Pre-flight validation endpoint."""
    try:
        data = request.get_json()
        if not data:
            return api_response(error="No data", status=400)
            
        subjects, teachers, periods = extract_request_data(data)
        validate_request_data(subjects, teachers, periods)
        return api_response(data={"valid": True})
    except TimetableError as e:
        return api_response(data={"valid": False, "error": e.message}, status=200)

@app.route("/export", methods=["POST"])
def export_csv() -> Response:
    """Export timetable to CSV."""
    try:
        data = request.get_json()
        timetable = data.get("timetable")
        if not timetable:
            return jsonify({"error": "No timetable data provided"}), 400
            
        csv_content = generate_csv(timetable)
        
        return Response(
            csv_content,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=timetable.csv"}
        )
    except Exception as e:
        logger.error(f"Export error: {e}")
        return jsonify({"error": "Failed to export CSV"}), 500

if __name__ == "__main__":
    logger.info(f"Starting server on port {PORT}, debug={DEBUG}")
    app.run(debug=DEBUG, port=PORT)
