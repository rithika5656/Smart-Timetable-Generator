
import pytest
from scheduler import Scheduler
from config import DEFAULT_PERIODS

def test_scheduler_initialization():
    subjects = ["Math", "Science"]
    teachers = ["Mr. A", "Ms. B"]
    scheduler = Scheduler(subjects, teachers, DEFAULT_PERIODS)
    assert scheduler.subjects == subjects
    assert scheduler.teachers == teachers
    assert len(scheduler.subject_teacher_map) == 2

def test_scheduler_empty_init():
    with pytest.raises(Exception):
        Scheduler([], [], DEFAULT_PERIODS)

def test_generate_standard():
    subjects = ["Math", "Science"]
    teachers = ["Mr. A", "Ms. B"]
    scheduler = Scheduler(subjects, teachers, 4)
    result = scheduler.generate()
    assert result.timetable is not None
    assert len(result.days) > 0
