"""
Smart Timetable Generator - Flask Web Application
"""

from flask import Flask, render_template, request, jsonify
from timetable_generator import generate_timetable

app = Flask(__name__)


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """API endpoint to generate timetable."""
    try:
        data = request.get_json()
        
        subjects = [s.strip() for s in data.get("subjects", "").split(",") if s.strip()]
        teachers = [t.strip() for t in data.get("teachers", "").split(",") if t.strip()]
        periods_per_day = int(data.get("periods_per_day", 6))
        
        if not subjects:
            return jsonify({"error": "Please enter at least one subject"}), 400
        
        if not teachers:
            return jsonify({"error": "Please enter at least one teacher"}), 400
        
        if periods_per_day < 1 or periods_per_day > 10:
            return jsonify({"error": "Periods per day must be between 1 and 10"}), 400
        
        result = generate_timetable(subjects, teachers, periods_per_day)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
