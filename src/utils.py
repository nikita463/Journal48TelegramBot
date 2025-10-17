import asyncio
from datetime import datetime
from typing import List,Optional
from datetime import date
from aiogram.types import User

from api.typings import Student, Day

async def run_at(run_time: datetime, coro, *args, **kwargs):
    now = datetime.now()
    delay = (run_time - now).total_seconds()
    if delay > 0:
        await asyncio.sleep(delay)
    try:
        return await coro(*args, **kwargs)
    except Exception as exp:
        print("[ERROR] run_every()" + str(exp))
        return None

async def run_every(interval: float, coro, *args, **kwargs):
    while True:
        try:
            await coro(*args, **kwargs)
        except Exception as exp:
            print("[ERROR] run_every()" + str(exp))
        await asyncio.sleep(interval)

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
    if user.id not in whitelistusers:
        print(f"Request from unknown user, id: {user.id}, username: {user.username}")
    return False
