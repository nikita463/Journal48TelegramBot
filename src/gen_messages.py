from datetime import date, timedelta
import locale
from typing import List
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils import find_by_date
from api.typings import Homework, Lesson, Day
from globals import weeks_diary, homeworks_list

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

def get_lesson_emoji(name: str) -> str:
    if name == "Иностранный язык (английский)":
        return "🇬🇧"
    elif name == "Химия":
        return "🧪"
    elif name == "Литература":
        return "📖"
    elif name == "Геометрия":
        return "📐"
    elif name == "История":
        return "📜"
    elif name == "Физика":
        return "🔬"
    elif name == "Обществознание":
        return "⚖️"
    elif name == "Алгебра и начала математического анализа":
        return "📘"
    elif name == "Биология":
        return "🧬"
    elif name == "География":
        return "🌍"
    elif name == "Русский язык":
        return "✍️"
    elif name == "Вероятность и статистика":
        return "📊"
    elif name == "Индивидуальный проект":
        return "📝"
    elif name == "Информатика" or name == "Информационная безопасность":
        return "💻"
    elif name == "Классный час":
        return "👥"
    elif name == "Разговоры о важном":
        return "💬"
    elif name == "Россия - мои горизонты":
        return "🌅"
    elif name == "Физическая культура":
        return "⚽"
    elif name == "Основы безопасности и защиты Родины":
        return "🇷🇺"
    else:
        print("Unexpected subject:", name)
        return ""

def gen_homework_description(homework: Homework) -> str:
    result = f"<i>{homework.text}</i>"
    for file in homework.files:
        result += f'\n  <a href="{file.link}">🖇 {file.filename}</a>'
    result += "\n"
    return result

def gen_lesson_description(lesson: Lesson, end_time: bool = False, room: bool = False, topic: bool = False, teacher: bool = False) -> str:
    result = ""
    lesson_emoji = get_lesson_emoji(lesson.name)
    if lesson.start:
        result += f"{lesson.start:%H:%M}"
        if end_time and lesson.end:
            result += f" - {lesson.end:%H:%M}"
        result += f" — "
    result += f"{lesson_emoji} <b>{lesson.name}</b>"

    if room:
        result += f"\n\n<b>Кабинет:</b> {lesson.room}\n"
    else:
        result += f" — <b>кабинет {lesson.room}</b>\n"
    if teacher: result += f"<b>Учитель:</b> {lesson.teacher}\n"
    if topic and len(lesson.topic) > 0: result += f"<b>Тема:</b> {lesson.topic}\n"
    if room or topic or teacher:
        result += "\n"

    if len(lesson.homeworks) > 0:
        result += "<blockquote>📝 <i>ДЗ:</i>"
        if len(lesson.homeworks) == 1:
            result += " " + gen_homework_description(lesson.homeworks[0])
        else:
            result += "\n"
            for homework in lesson.homeworks:
                result += "• " + gen_homework_description(homework)
        result += "</blockquote>"
    return result

def gen_day_title(dt: date, name: str) -> str:
    formatted_date = dt.strftime("%A, %d %B %Y")
    formatted_date = formatted_date[0].upper() + formatted_date[1:]
    if name != "":
        return "📅 <b>" + name + " — " + formatted_date + "</b>"
    return "📅 <b>" + formatted_date + "</b>"

def gen_diary(day: Day, name: str) -> str:
    result = gen_day_title(day.date, name) + "\n"
    for i, lesson in enumerate(day.lessons):
        result += f"\n{i + 1}) " + gen_lesson_description(lesson)
    return result

def get_day_name(dt: date, upper: bool) -> str:
    if dt == date.today() - timedelta(days=2):
        return "Позавчера" if upper else "позавчера"
    elif dt == date.today() - timedelta(days=1):
        return "Вчера" if upper else "вчера"
    elif dt == date.today():
        return "Сегодня" if upper else "сегодня"
    elif dt == date.today() + timedelta(days=1):
        return "Завтра" if upper else "завтра"
    elif dt == date.today() + timedelta(days=2):
        return "Послезавтра" if upper else "послезавтра"
    else:
        return ""

def gen_day_diary(dt: date, student_name: str) -> str:
    day = find_by_date(weeks_diary, dt, student_name)
    name = get_day_name(dt, True)
    if day is None:
        result = gen_day_title(dt, name) + "\n\n"
        result += "На этот день уроков нет\n"
        return result
    return gen_diary(day, name)

def gen_today_diary(student_name: str) -> dict:
    return {
        "text": gen_day_diary(date.today(), student_name),
        "parse_mode": "HTML"
    }

def gen_tomorrow_diary(student_name: str) -> dict:
    return {
        "text": gen_day_diary(date.today() + timedelta(days=1), student_name),
        "parse_mode": "HTML"
    }

def gen_week_diary_msg(selected_date: date, student_name: str) -> dict:
    monday = selected_date - timedelta(days=selected_date.weekday())
    if selected_date.weekday() >= 5:
        monday += timedelta(weeks=1)
        selected_date = monday

    date_buttons = []
    for i in range(0, 5):
        curr_date = monday + timedelta(days=i)
        if i == selected_date.weekday():
            text = "🟢 " + curr_date.strftime("%d %b")
        else:
            text = curr_date.strftime("%d %b")
        button = InlineKeyboardButton(
            text=text,
            callback_data=f"week_timetable_" + curr_date.isoformat()
        )
        date_buttons.append(button)

    current_monday = date.today() - timedelta(days=date.today().weekday())
    if current_monday == monday:
        change_week_button = InlineKeyboardButton(
            text="Следующая неделя",
            callback_data=f"week_timetable_" + (monday + timedelta(weeks=1)).isoformat()
        )
    else:
        next_week_date = date.today()
        if date.today().weekday() >= 5:
            next_week_date = current_monday + timedelta(days=4)
        change_week_button = InlineKeyboardButton(
            text="Текущая неделя",
            callback_data=f"week_timetable_" + next_week_date.isoformat()
        )

    lessons_button_tip = InlineKeyboardButton(text="Подробности уроков", callback_data="tip_lesson_detail")

    lessons_buttons = []
    day = find_by_date(weeks_diary, selected_date, student_name)
    if day:
        for lesson in day.lessons:
            lessons_buttons.append(InlineKeyboardButton(
                text=lesson.num,
                callback_data=f"lesson_detail_week_{int(lesson.num) - 1}_{selected_date.isoformat()}"
            ))

    text = gen_day_diary(selected_date, student_name)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [lessons_button_tip],
        lessons_buttons,
        date_buttons[:2],
        date_buttons[2:],
        [change_week_button]
    ])

    return {
        "text": text,
        "reply_markup": keyboard,
        "parse_mode": "HTML"
    }


def gen_day_homeworks_list(dt: date, student_name: str) -> str:
    result = "📝 <b>Домашние задания на "
    name = get_day_name(dt, False)
    if name != "":
        result += name + ", "
    result += dt.strftime("%d %B %Y").lower() + "</b>\n\n"

    hw_lessons: List[Lesson] = []
    for lesson in homeworks_list[student_name]:
        if lesson.date == dt:
            hw_lessons.append(lesson)
    for lesson in sorted(hw_lessons, key=lambda x: (x.date, x.start)):
        result += f"{lesson.num}) " + gen_lesson_description(lesson) + "\n"

    return result

def gen_week_homeworks_list(selected_date: date, student_name: str) -> dict:
    monday = selected_date - timedelta(days=selected_date.weekday())
    if selected_date.weekday() >= 5:
        monday += timedelta(weeks=1)
        selected_date = monday

    date_buttons = []
    for i in range(0, 5):
        if i == selected_date.weekday():
            text = "🟢 " + (monday + timedelta(days=i)).strftime("%d %b")
        else:
            text = (monday + timedelta(days=i)).strftime("%d %b")
        button = InlineKeyboardButton(
            text=text,
            callback_data=f"homeworks_list_" + (monday + timedelta(days=i)).isoformat()
        )
        date_buttons.append(button)

    current_monday = date.today() - timedelta(days=date.today().weekday())
    if current_monday == monday:
        change_week_button = InlineKeyboardButton(
            text="Следующая неделя",
            callback_data=f"homeworks_list_" + (monday + timedelta(weeks=1)).isoformat()
        )
    else:
        next_week_date = date.today()
        if date.today().weekday() >= 5:
            next_week_date = current_monday + timedelta(days=4)
        change_week_button = InlineKeyboardButton(
            text="Текущая неделя",
            callback_data=f"homeworks_list_" + next_week_date.isoformat()
        )

    lessons_button_tip = InlineKeyboardButton(text="Подробности уроков", callback_data="tip_lesson_detail")

    lessons_buttons = []
    for lesson in homeworks_list[student_name]:
        if lesson.date == selected_date:
            lessons_buttons.append(InlineKeyboardButton(
                text=lesson.num,
                callback_data=f"lesson_detail_homework_{int(lesson.num) - 1}_{selected_date.isoformat()}"
            ))

    text = gen_day_homeworks_list(selected_date, student_name)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [lessons_button_tip],
        lessons_buttons,
        date_buttons[:2],
        date_buttons[2:],
        [change_week_button]
    ])

    return {
        "text": text,
        "reply_markup": keyboard,
        "parse_mode": "HTML"
    }


def gen_lesson_detail(dt: date, lesson_num: int, prev_msg: str, student_name: str) -> dict:
    lesson = find_by_date(weeks_diary, dt, student_name).lessons[lesson_num]

    result = f"<b>📚 {lesson.num}-й урок — "
    name = get_day_name(lesson.date, False)
    if name != "":
        result += f"{name}, "
    result += lesson.date.strftime("%d %B %Y").lower() + "</b>\n\n"
    result += gen_lesson_description(lesson, end_time=True, room=True, topic=True, teacher=True)

    return_button = None
    if prev_msg == "homework":
        return_button = InlineKeyboardButton(
            text="Назад",
            callback_data=f"homeworks_list_{lesson.date.isoformat()}"
        )
    elif prev_msg == "week":
        return_button = InlineKeyboardButton(
            text="Назад",
            callback_data=f"week_timetable_{lesson.date.isoformat()}"
        )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [return_button]
    ])

    return {
        "text": result,
        "reply_markup": keyboard,
        "parse_mode": "HTML"
    }
