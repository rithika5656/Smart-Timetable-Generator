"""
Utility functions for input validation and data extraction.
"""
from typing import Dict, List, Tuple, Any
from flask import jsonify, Response

from config import DEFAULT_PERIODS, MIN_PERIODS, MAX_PERIODS, MAX_SUBJECTS, MAX_TEACHERS
from exceptions import TimetableError

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

def generate_csv(timetable: Dict[str, List[Dict[str, Any]]]) -> str:
    """
    Convert timetable JSON structure to CSV string.
    
    Args:
        timetable: The timetable dictionary {day: [sessions]}.
        
    Returns:
        CSV formatted string.
    """
    import io
    import csv
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    headers = ["Day", "Period", "Subject", "Teacher"]
    writer.writerow(headers)
    
    # Rows
    for day, sessions in timetable.items():
        for session in sessions:
            writer.writerow([
                day,
                session['period'],
                session['subject'],
                session['teacher']
            ])
            
    return output.getvalue()
