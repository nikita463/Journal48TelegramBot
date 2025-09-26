from api.typings import date, Day, Student
from typing import List, Optional
from aiogram.types import User

def find_by_date(students: List[Student], target_date: date, student_name) -> Optional[Day]:
    for student in students:
        if student.name == student_name:
            for day in student.days:
                if day.date == target_date:
                    return day
    return None

def get_message_args(text: str) -> set:
    args = text.split()
    return {*args[1:]} if len(args) > 0 else {}

def check_user(user: User, whitelistusers) -> bool:
    if user.id not in whitelistusers: return True
    return False
