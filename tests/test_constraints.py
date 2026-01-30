"""
Tests for constraint engine.
"""
import pytest
from constraints import MaxConsecutivePeriods, TeacherDailyLimit
from models import ClassSession, SessionType

def test_max_consecutive_violation():
    rule = MaxConsecutivePeriods(max_periods=1)
    
    # Create valid schedule
    schedule_valid = {
        "Monday": [
            ClassSession(1, "Math", "Teacher A"),
            ClassSession(2, "Physics", "Teacher B")
        ]
    }
    violations = rule.validate(schedule_valid, {"teachers": ["Teacher A", "Teacher B"]})
    assert len(violations) == 0
    
    # Create invalid schedule
    schedule_invalid = {
        "Monday": [
            ClassSession(1, "Math", "Teacher A"),
            ClassSession(2, "Math", "Teacher A")
        ]
    }
    violations = rule.validate(schedule_invalid, {"teachers": ["Teacher A"]})
    assert len(violations) > 0

def test_daily_limit_violation():
    rule = TeacherDailyLimit(max_daily=1)
    
    schedule = {
        "Monday": [
            ClassSession(1, "Math", "Teacher A"),
            ClassSession(2, "Science", "Teacher A")
        ]
    }
    violations = rule.validate(schedule, {})
    assert len(violations) > 0
