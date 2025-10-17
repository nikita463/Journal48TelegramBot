from dataclasses import dataclass, field
from datetime import date, time
from typing import List

@dataclass
class File:
    filename: str = ""
    link: str = ""

@dataclass
class Homework:
    id: int = 0
    text: str = ""
    individual: bool = False
    files: List[File] = field(default_factory=list)

@dataclass
class Lesson:
    name: str = ""
    date: date = date(2000, 1, 1)
    homeworks: List[Homework] = field(default_factory=list)
    id: int = 0
    num: int = 0
    room: str = ""
    teacher: str = ""
    start: time | None = None
    end: time | None = None

@dataclass
class Day:
    date: date = date(2000, 1, 1)
    title: str = ""
    lessons: List[Lesson] = field(default_factory=list)

@dataclass
class Student:
    name: str = ""
    title: str = ""
    days: List[Day] = field(default_factory=list)

@dataclass
class Vendor:
    vendor_id: int = 0
    vendor_title: str = ""
    vendor: str = ""
    token: str = ""
    user_title: str = ""
    expires: str = ""
    login: str = ""
