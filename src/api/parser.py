from .typings import Day, Lesson, Homework, File, Vendor, Student
from typing import List, Dict, Any
from datetime import datetime
from zoneinfo import ZoneInfo
from copy import deepcopy

def parse_homeworks(js: Dict[str, Any]) -> List[Homework]:
    jsHomeworks = {}
    for key in js["homework"]:
        hw_id = js["homework"][key]["id"]
        text = js["homework"][key]["value"]
        individual = js["homework"][key]["individual"]
        jsHomeworks[hw_id] = {"id": hw_id, "text": text, "individual": individual, "files": []}
    for file in js["files"]:
        toid = file["toid"]
        filename = file["filename"]
        link = file["link"]
        file = {
            "filename": filename,
            "link": link
        }
        jsHomeworks[toid]["files"].append(file)

    result = []
    for hw_key in jsHomeworks:
        homework = deepcopy(Homework(**jsHomeworks[hw_key]))
        homework.files = []
        for jsFile in jsHomeworks[hw_key]["files"]:
            homework.files.append(File(**jsFile))
        result.append(homework)

    return result

def parse_lesson(js: Dict[str, Any]) -> Lesson:
    result = Lesson(
        lesson_id=js["lesson_id"],
        name=js["name"],
        num=js["num"],
        room=js["room"],
        teacher=js["teacher"]
    )

    if "starttime" in js and "endtime" in js:
        result.start = datetime.strptime(js["starttime"], "%H:%M:%S").time()
        result.end = datetime.strptime(js["endtime"], "%H:%M:%S").time()

    result.homeworks = parse_homeworks(js)

    return result

def parse_day(js: Dict[str, Any]) -> Day:
    dt = datetime.strptime(js["name"], "%Y%m%d")
    msk_tz = ZoneInfo("Europe/Moscow")
    dt = dt.replace(tzinfo=msk_tz).date()

    result = Day(date=dt, title=js["title"])

    for key in js["items"]:
        item = js["items"][key]
        result.lessons.append(parse_lesson(item))

    return result

def parse_student(js: Dict[str, Any]) -> Student:
    return Student(
        name=js["name"],
        title=js["title"],
        days=[parse_day(js["days"][e]) for e in js["days"]]
    )

def parse_diary(js: Dict[str, Any]) -> List[Student]:
    result = []
    for key, elem in js["response"]["result"]["students"].items():
        result.append(parse_student(elem))
    return result

def parse_vendors(js: Dict[str, Any]) -> List[Vendor]:
    result: List[Vendor] = []
    for e in js["result"]:
        result.append(Vendor(**e))
    return result
