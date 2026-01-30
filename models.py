"""
Data models for the timetable scheduler.
"""
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any

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

    def __str__(self) -> str:
        return f"{self.subject} ({self.teacher})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "period": self.period,
            "subject": self.subject,
            "teacher": self.teacher,
            "type": self.type.value
        }

@dataclass
class TimetableResult:
    """Result of the scheduling process."""
    timetable: Dict[str, List[Dict[str, Any]]]
    time_slots: List[str]
    days: List[str]
    subject_teacher_map: Dict[str, str]
    meta: Dict[str, Any] = None

@dataclass
class HistoryEntry:
    """Represents a generation history record."""
    id: int
    timestamp: str
    subjects: int
    teachers: int
    duration: float

@dataclass
class ConstraintViolation:
    """Represents a rule violation."""
    rule: str
    message: str
