import asyncio
from api.api import get_diary, get_vendors
from api.typings import List, Student
from typing import Dict, Any
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dataclasses import dataclass
import json

TZ = ZoneInfo("Europe/Moscow")

@dataclass
class Data:
    v_token: str
    student_name: str

data: Data | None = None
weeks_diary: List[Student] = []

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

async def load_data(json_path: str):
    global data
    with open(json_path, "rb") as f:
        data = Data(**json.load(f))

async def update_diary():
    print("diary update")
    global weeks_diary

    vendor = await get_vendors(data.v_token)
    vendor = vendor[0]

    today = datetime.now(TZ).date()
    weekday = today.weekday()

    start_of_current_week = (today - timedelta(days=weekday))
    end_of_current_week = start_of_current_week + timedelta(days=6)
    start_of_next_week = start_of_current_week + timedelta(days=7)
    end_of_next_week = start_of_next_week + timedelta(days=6)

    weeks_diary.clear()
    weeks_diary.extend(await get_diary(start_of_current_week, end_of_current_week, vendor))
    weeks_diary.extend(await get_diary(start_of_next_week, end_of_next_week, vendor))

async def run_update_diary(interval: float):
    asyncio.create_task(run_every(interval, update_diary))
