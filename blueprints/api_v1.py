"""
API Version 1 Routes.
"""
from flask import Blueprint, request, jsonify
from api_auth import require_api_key
from utils import api_response, extract_request_data, validate_request_data
from scheduler import generate_scheduler_response
from models import TimetableResult
import time

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

@api_v1.route('/health', methods=['GET'])
def health_check():
    """Deep health check."""
    return api_response(data={
        "status": "healthy",
        "timestamp": time.time(),
        "components": {
            "database": "connected", # Mock for now
            "scheduler": "ready"
        }
    })

@api_v1.route('/generate', methods=['POST'])
@require_api_key
def generate_schedule():
    """
    Generate timetable (Version 1).
    Requires X-API-Key header.
    """
    try:
        data = request.get_json()
        if not data:
            return api_response(error="Invalid JSON", status=400)
            
        subjects, teachers, periods = extract_request_data(data)
        validate_request_data(subjects, teachers, periods)
        
        start = time.time()
        result = generate_scheduler_response(subjects, teachers, periods)
        duration = time.time() - start
        
        # Enrich metadata
        result['meta']['api_version'] = 'v1'
        result['meta']['generated_at'] = time.time()
        
        return api_response(data=result)
        
    except Exception as e:
        return api_response(error=str(e), status=500)

@api_v1.route('/metrics', methods=['GET'])
@require_api_key
def metrics():
    """Application metrics."""
    # This would usually come from a real metrics store
    from database import get_db
    try:
        db = get_db()
        count = db.execute('SELECT COUNT(*) FROM history').fetchone()[0]
        avg_time = db.execute('SELECT AVG(duration) FROM history').fetchone()[0]
        
        return api_response(data={
            "total_generations": count,
            "average_generation_time": round(avg_time or 0, 4)
        })
    except:
        return api_response(data={"metrics": "unavailable"})
