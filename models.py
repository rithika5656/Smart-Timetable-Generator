"""
Data models for the timetable scheduler.
"""
from dataclasses import dataclass
from enum import Enum
from typing import List

class DayOfWeek(str, Enum):
    """Enumeration of days of the week."""
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class SessionType(str, Enum):
    """Type of session."""
    LECTURE = "Lecture"
    BREAK = "Break"

@dataclass
class ClassSession:
    """Represents a single class session."""
    period: int
    subject: str
    teacher: str
    type: SessionType = SessionType.LECTURE

@dataclass
class TimetableResult:
    """Represents the final generated timetable result."""
    timetable: dict
    time_slots: List[str]
    days: List[str]
    subject_teacher_map: dict
    meta: dict = None
