import asyncio
from typing import Dict
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dataclasses import dataclass
import json

from api.api import get_diary, get_vendors
from api.typings import Student, Lesson
from utils import run_every, get_homeworks_dict

TZ = ZoneInfo("Europe/Moscow")

@dataclass
class Data:
    v_token: str
    student_name: str

data: Data | None = None
weeks_diary: Dict[str, Student] = dict()
homeworks_dict: Dict[str, Dict[int, Lesson]] = dict()

async def load_data(json_path: str):
    global data
    with open(json_path, "rb") as f:
        data = Data(**json.load(f))

async def update_diary():
    global weeks_diary

    vendor = await get_vendors(data.v_token)
    if vendor is None:
        print("[ERROR] update_diary(): vendor not received")
        return
    vendor = vendor[0]

    today = datetime.now(TZ).date()
    weekday = today.weekday()

    start_of_current_week = (today - timedelta(days=weekday))
    end_of_current_week = start_of_current_week + timedelta(days=6)
    start_of_next_week = start_of_current_week + timedelta(days=7)
    end_of_next_week = start_of_next_week + timedelta(days=6)

    current_week_diary = await get_diary(start_of_current_week, end_of_current_week, vendor, data.student_name)
    next_week_diary = await get_diary(start_of_next_week, end_of_next_week, vendor, data.student_name)
    if current_week_diary is None:
        print("[ERROR] update_diary(): current_week_diary not received")
        return
    if next_week_diary is None:
        print("[ERROR] update_diary(): next_week_diary not received")
        return

    weeks_diary.clear()
    weeks_diary.update(current_week_diary)

    for key, new_student in next_week_diary.items():
        if key in weeks_diary:
            existing = weeks_diary[key]
            existing.days.extend(new_student.days)
        else:
            weeks_diary[key] = new_student

    homeworks_dict.clear()
    for student_name, student in weeks_diary.items():
        homeworks_dict.update({student_name: get_homeworks_dict(student)})

    print("diary updated")

async def run_update_diary(interval: float):
    asyncio.create_task(run_every(interval, update_diary))
