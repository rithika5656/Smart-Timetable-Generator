"""
Robust scheduler for generating conflict-free timetables.
"""
import random
import logging
from typing import List, Dict, Optional, Any

from config import DEFAULT_PERIODS, START_HOUR, DEFAULT_DAYS
from models import DayOfWeek, ClassSession, TimetableResult
from exceptions import TimetableError

logger = logging.getLogger(__name__)

class Scheduler:
    """
    Core engine for generating timetables.
    """
    def __init__(self, subjects: List[str], teachers: List[str], periods_per_day: int):
        self.subjects = subjects
        self.teachers = teachers
        self.periods_per_day = periods_per_day
        self.days = [d.value for d in DayOfWeek if d.value in DEFAULT_DAYS]
        
        # Validation checks rely on upstream validation in utils.py
        # but we add a safety check here too.
        if not self.subjects or not self.teachers:
            raise TimetableError("Scheduler requires subjects and teachers")

        self.subject_teacher_map = self._assign_teachers()

    def _assign_teachers(self) -> Dict[str, str]:
        """Round-robin assignment of subjects to teachers."""
        mapping = {}
        for i, subject in enumerate(self.subjects):
            mapping[subject] = self.teachers[i % len(self.teachers)]
        return mapping

    def _generate_pools(self) -> List[str]:
        """Create a distributed pool of subjects."""
        total_slots = len(self.days) * self.periods_per_day
        slots_per_subject = total_slots // len(self.subjects)
        
        pool = []
        for subject in self.subjects:
            pool.extend([subject] * slots_per_subject)
            
        # Fill remainder
        remaining = total_slots - len(pool)
        for _ in range(remaining):
            pool.append(random.choice(self.subjects))
            
        random.shuffle(pool)
        return pool

    def _distribute_slots(self, pool: List[str]) -> Dict[str, List[ClassSession]]:
        """Distribute the pool across days and periods."""
        timetable = {}
        idx = 0
        
        for day in self.days:
            daily_schedule = []
            for p in range(self.periods_per_day):
                if idx >= len(pool):
                    break # Should not happen if math is right
                    
                subject = pool[idx]
                session = ClassSession(
                    period=p + 1,
                    subject=subject,
                    teacher=self.subject_teacher_map[subject]
                )
                daily_schedule.append(session)
                idx += 1
            timetable[day] = daily_schedule
            
        return timetable

    def _optimize(self, timetable: Dict[str, List[ClassSession]]) -> Dict[str, List[ClassSession]]:
        """Reduce consecutive duplicate subjects."""
        swaps = 0
        for day, sessions in timetable.items():
            for i in range(len(sessions) - 1):
                current = sessions[i]
                next_session = sessions[i+1]
                
                if current.subject == next_session.subject:
                    # Look for swap candidate
                    for j in range(i + 2, len(sessions)):
                        candidate = sessions[j]
                        if candidate.subject != current.subject:
                            # Swap objects
                            sessions[i+1], sessions[j] = sessions[j], sessions[i+1]
                            # Fix period numbers after swap
                            sessions[i+1].period = i + 2
                            sessions[j].period = j + 1
                            swaps += 1
                            break
        
        logger.info(f"Optimization completed with {swaps} swaps")
        return timetable

    def _generate_time_slots(self) -> List[str]:
        """Generate human-readable time strings."""
        slots = []
        for i in range(self.periods_per_day):
            hour = START_HOUR + i
            start_str = f"{hour}:00 {'AM' if hour < 12 else 'PM'}"
            # Simple logic for 50 min periods
            slots.append(f"Period {i+1} ({start_str})") 
        return slots

    def generate(self) -> TimetableResult:
        """Execute the generation pipeline."""
        pool = self._generate_pools()
        raw_schedule = self._distribute_slots(pool)
        optimized_schedule = self._optimize(raw_schedule)
        time_slots = self._generate_time_slots()
        
        # Convert ClassSession objects to dicts for JSON serialization
        # This is a bit of a hack for simple JSON serialization compatibility
        serializable_schedule = {}
        for day, sessions in optimized_schedule.items():
            serializable_schedule[day] = [
                {"period": s.period, "subject": s.subject, "teacher": s.teacher}
                for s in sessions
            ]

        return TimetableResult(
            timetable=serializable_schedule,
            time_slots=time_slots,
            days=self.days,
            subject_teacher_map=self.subject_teacher_map
        )

def generate_scheduler_response(subjects: List[str], teachers: List[str], periods: int) -> Dict[str, Any]:
    """Public interface for the scheduling engine."""
    scheduler = Scheduler(subjects, teachers, periods)
    result = scheduler.generate()
    
    return {
        "timetable": result.timetable,
        "time_slots": result.time_slots,
        "days": result.days,
        "subject_teacher_map": result.subject_teacher_map
    }
