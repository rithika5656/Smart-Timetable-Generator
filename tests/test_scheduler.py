"""
Unit tests for the Scheduler class.
"""
import pytest
from scheduler import Scheduler
from exceptions import TimetableError

def test_scheduler_initialization(sample_data):
    """Test that scheduler initializes correctly."""
    s = Scheduler(sample_data["subjects"], sample_data["teachers"], sample_data["periods"])
    assert s.periods_per_day == 6
    assert len(s.subjects) == 3
    assert len(s.teachers) == 3

def test_generate_pools(sample_data):
    """Test that subject pool is generated correctly."""
    s = Scheduler(sample_data["subjects"], sample_data["teachers"], sample_data["periods"])
    pool = s._generate_pools()
    
    # Total slots = 5 days * 6 periods = 30
    assert len(pool) == 30
    # Each subject should appear roughly equal times
    assert pool.count("Math") >= 9

def test_optimize(sample_data):
    """Test that optimization runs without error."""
    s = Scheduler(sample_data["subjects"], sample_data["teachers"], sample_data["periods"])
    result = s.generate()
    assert result.timetable is not None
    assert "Monday" in result.timetable

def test_invalid_inputs():
    """Test validation."""
    with pytest.raises(TimetableError):
        Scheduler([], [], 6)
