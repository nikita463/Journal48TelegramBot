from datetime import date, timedelta
import locale
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils import find_by_date
from api.typings import Homework, Lesson, Day
from globals import weeks_diary

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

def gen_homework_description(homework: Homework):
    result = f"<i>{homework.text}</i>"
    for file in homework.files:
        result += f'\n  <a href="{file.link}">🖇 {file.filename}</a>'
    result += "\n"
    return result

def gen_lesson_description(lesson: Lesson):
    result = ""
    lesson_emoji = get_lesson_emoji(lesson.name)
    if lesson.start:
        result += f"{lesson.start:%H:%M} — {lesson_emoji} <b>{lesson.name}</b> — <b>кабинет {lesson.room}</b>\n"
    else:
        result += f"{lesson_emoji} <b>{lesson.name}</b> — <b>кабинет {lesson.room}</b>\n"
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

def gen_day_title(dt: date, name: str):
    formatted_date = dt.strftime("%A, %d %b %Y")
    formatted_date = formatted_date[0].upper() + formatted_date[1:]
    if name != "":
        return "📅 <b>" + name + " — " + formatted_date + "</b>"
    return "📅 <b>" + formatted_date + "</b>"

def gen_diary(day: Day, name: str) -> str:
    result = gen_day_title(day.date, name) + "\n"
    for i, lesson in enumerate(day.lessons):
        result += f"\n{i + 1}) " + gen_lesson_description(lesson)
    return result

def gen_day_diary(dt: date, student_name: str):
    day = find_by_date(weeks_diary, dt, student_name)
    name = ""
    if dt == date.today() - timedelta(days=2):
        name = "Позавчера"
    elif dt == date.today() - timedelta(days=1):
        name = "Вчера"
    elif dt == date.today():
        name = "Сегодня"
    elif dt == date.today() + timedelta(days=1):
        name = "Завтра"
    elif dt == date.today() + timedelta(days=2):
        name = "Послезавтра"
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

def gen_week_diary_msg(next_date: date, student_name: str) -> dict:
    st_day = next_date.weekday()
    monday = next_date - timedelta(days=next_date.weekday())
    if st_day >= 5:
        st_day = 0
        monday += timedelta(weeks=1)

    date_buttons = []
    for i in range(0, 5):
        if i == st_day:
            text = "🟢 " + (monday + timedelta(days=i)).strftime("%d %b")
        else:
            text = (monday + timedelta(days=i)).strftime("%d %b")
        button = InlineKeyboardButton(
            text=text,
            callback_data=f"week_timetable_" + (monday + timedelta(days=i)).isoformat()
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
            text="Предыдущая неделя",
            callback_data=f"week_timetable_" + next_week_date.isoformat()
        )

    text = gen_day_diary(monday + timedelta(st_day), student_name)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[date_buttons[:2], date_buttons[2:], [change_week_button]])

    return {
        "text": text,
        "reply_markup": keyboard,
        "parse_mode": "HTML"
    }
