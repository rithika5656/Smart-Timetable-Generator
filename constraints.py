"""
Constraint Rules Engine.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from models import ClassSession

class Constraint(ABC):
    @abstractmethod
    def validate(self, schedule: Dict[str, List[ClassSession]], meta: Dict[str, Any]) -> List[str]:
        """Return list of violation messages."""
        pass

class MaxConsecutivePeriods(Constraint):
    """Rule: Teachers should not have too many consecutive periods."""
    def __init__(self, max_periods: int = 2):
        self.max_periods = max_periods

    def validate(self, schedule: Dict[str, List[ClassSession]], meta: Dict[str, Any]) -> List[str]:
        violations = []
        for day, sessions in schedule.items():
            # Sort by period to be sure
            sessions.sort(key=lambda x: x.period)
            
            for teacher in meta.get('teachers', []):
                consecutive = 0
                for session in sessions:
                    if session.type == 'Lecture' and session.teacher == teacher:
                        consecutive += 1
                    else:
                        consecutive = 0
                    
                    if consecutive > self.max_periods:
                        violations.append(f"{teacher} exceeds {self.max_periods} consecutive periods on {day}")
                        # Reset to avoid spamming violations for the same sequence
                        consecutive = 0 
        return violations

class TeacherDailyLimit(Constraint):
    """Rule: Teachers should not exceed max daily sessions."""
    def __init__(self, max_daily: int = 4):
        self.max_daily = max_daily

    def validate(self, schedule: Dict[str, List[ClassSession]], meta: Dict[str, Any]) -> List[str]:
        violations = []
        for day, sessions in schedule.items():
            teacher_daily_count = {}
            for session in sessions:
                if session.teacher not in teacher_daily_count:
                    teacher_daily_count[session.teacher] = 0
                if session.type == 'Lecture':
                    teacher_daily_count[session.teacher] += 1
            
            for teacher, count in teacher_daily_count.items():
                if count > self.max_daily:
                    violations.append(f"{teacher} has {count} classes on {day} (Max: {self.max_daily})")
        return violations
