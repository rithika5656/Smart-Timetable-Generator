"""
Smart Timetable Generator Algorithm
Generates conflict-free class timetables automatically
"""

import random
from typing import List, Dict

class TimetableGenerator:
    def __init__(self, subjects: List[str], teachers: List[str], 
                 days: List[str] = None, periods_per_day: int = 6):
        """
        Initialize the timetable generator.
        
        Args:
            subjects: List of subject names
            teachers: List of teacher names
            days: List of days (default: Monday to Friday)
            periods_per_day: Number of periods per day
        """
        self.subjects = subjects
        self.teachers = teachers
        self.days = days or ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.periods_per_day = periods_per_day
        
        # Map subjects to teachers (round-robin assignment)
        self.subject_teacher_map = {}
        for i, subject in enumerate(subjects):
            teacher_index = i % len(teachers)
            self.subject_teacher_map[subject] = teachers[teacher_index]
    
    def generate(self) -> Dict:
        """
        Generate a timetable using constraint-based scheduling.
        
        Returns:
            Dictionary containing the generated timetable
        """
        timetable = {day: [] for day in self.days}
        
        # Calculate how many times each subject should appear per week
        total_slots = len(self.days) * self.periods_per_day
        slots_per_subject = total_slots // len(self.subjects)
        
        # Create a pool of subjects to distribute
        subject_pool = []
        for subject in self.subjects:
            subject_pool.extend([subject] * slots_per_subject)
        
        # Fill remaining slots with random subjects
        remaining_slots = total_slots - len(subject_pool)
        for _ in range(remaining_slots):
            subject_pool.append(random.choice(self.subjects))
        
        # Shuffle the pool for randomness
        random.shuffle(subject_pool)
        
        # Distribute subjects across the timetable
        pool_index = 0
        for day in self.days:
            day_schedule = []
            for period in range(self.periods_per_day):
                subject = subject_pool[pool_index]
                teacher = self.subject_teacher_map[subject]
                day_schedule.append({
                    "period": period + 1,
                    "subject": subject,
                    "teacher": teacher
                })
                pool_index += 1
            timetable[day] = day_schedule
        
        # Optimize to reduce consecutive same subjects
        timetable = self._optimize_timetable(timetable)
        
        return timetable
    
    def _optimize_timetable(self, timetable: Dict) -> Dict:
        """
        Optimize the timetable to reduce consecutive same subjects.
        
        Args:
            timetable: The initial timetable
            
        Returns:
            Optimized timetable
        """
        for day in self.days:
            schedule = timetable[day]
            # Try to swap consecutive same subjects
            for i in range(len(schedule) - 1):
                if schedule[i]["subject"] == schedule[i + 1]["subject"]:
                    # Find a different subject to swap with
                    for j in range(i + 2, len(schedule)):
                        if schedule[j]["subject"] != schedule[i]["subject"]:
                            # Swap
                            schedule[i + 1], schedule[j] = schedule[j], schedule[i + 1]
                            # Update period numbers
                            schedule[i + 1]["period"] = i + 2
                            schedule[j]["period"] = j + 1
                            break
        
        return timetable
    
    def get_time_slots(self) -> List[str]:
        """
        Generate time slots for the timetable.
        
        Returns:
            List of time slot strings
        """
        start_hour = 9  # 9 AM
        slots = []
        for i in range(self.periods_per_day):
            hour = start_hour + i
            if hour < 12:
                slots.append(f"{hour}:00 AM - {hour}:50 AM")
            elif hour == 12:
                slots.append(f"12:00 PM - 12:50 PM")
            else:
                slots.append(f"{hour-12}:00 PM - {hour-12}:50 PM")
        return slots


def generate_timetable(subjects: List[str], teachers: List[str], 
                       periods_per_day: int = 6) -> Dict:
    """
    Convenience function to generate a timetable.
    
    Args:
        subjects: List of subject names
        teachers: List of teacher names
        periods_per_day: Number of periods per day
        
    Returns:
        Dictionary containing the timetable and metadata
    """
    generator = TimetableGenerator(subjects, teachers, periods_per_day=periods_per_day)
    timetable = generator.generate()
    time_slots = generator.get_time_slots()
    
    return {
        "timetable": timetable,
        "time_slots": time_slots,
        "days": generator.days,
        "subject_teacher_map": generator.subject_teacher_map
    }


# Example usage
if __name__ == "__main__":
    subjects = ["Mathematics", "Physics", "Chemistry", "English", "Computer Science"]
    teachers = ["Mr. Smith", "Ms. Johnson", "Mr. Brown", "Ms. Davis", "Mr. Wilson"]
    
    result = generate_timetable(subjects, teachers)
    
    print("Generated Timetable:")
    print("=" * 50)
    for day, schedule in result["timetable"].items():
        print(f"\n{day}:")
        for slot in schedule:
            print(f"  Period {slot['period']}: {slot['subject']} ({slot['teacher']})")
