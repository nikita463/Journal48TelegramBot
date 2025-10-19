import asyncio
from datetime import date
from dotenv import load_dotenv
from os import getenv

import globals
from gen_messages import gen_today_diary, gen_tomorrow_diary, gen_week_diary_msg, gen_week_homeworks_list, gen_lesson_detail
from utils import check_user, find_by_date

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

load_dotenv(".env")
token = getenv("BOT_TOKEN", "")
whitelistusers = list(map(int, getenv("WHITELISTUSERS", "").split(",")))
bot = Bot(token)
dp = Dispatcher()

@dp.message(Command("start"))
async def handle_start(message: Message):
    if check_user(message.from_user, whitelistusers): return

    text = ("/today - Расписание на сегодня\n"
            "/tomorrow - Расписание на завтра\n"
            "/week - расписание на неделю")
    await message.answer(text)

@dp.message(Command("today"))
async def handle_today_timetable(message: Message):
    if check_user(message.from_user, whitelistusers): return

    await message.answer(**gen_today_diary(globals.data.student_name))

@dp.message(Command("tomorrow"))
async def handle_tomorrow_timetable(message: Message):
    if check_user(message.from_user, whitelistusers): return

    await message.answer(**gen_tomorrow_diary(globals.data.student_name))

@dp.message(Command("week"))
async def handle_week_timetable(message: Message):
    if check_user(message.from_user, whitelistusers): return

    await message.answer(**gen_week_diary_msg(date.today(), globals.data.student_name))

@dp.callback_query(F.data.startswith("week_timetable"))
async def callback_week_timetable(callback: CallbackQuery):
    if check_user(callback.from_user, whitelistusers): return

    callback_data = callback.data.removeprefix("week_timetable_")
    next_date = date.fromisoformat(callback_data)

    await callback.answer()
    try:
        await callback.message.edit_text(**gen_week_diary_msg(next_date, globals.data.student_name))
    except TelegramBadRequest as exp:
        if "message is not modified" not in exp.message:
            print("[ERROR]", exp.message)


@dp.message(Command("homework"))
async def handle_week_homeworks_list(message: Message):
    if check_user(message.from_user, whitelistusers): return

    await message.answer(**gen_week_homeworks_list(date.today(), globals.data.student_name))

@dp.callback_query(F.data.startswith("homeworks_list"))
async def callback_week_timetable(callback: CallbackQuery):
    if check_user(callback.from_user, whitelistusers): return

    callback_data = callback.data.removeprefix("homeworks_list_")
    next_date = date.fromisoformat(callback_data)

    await callback.answer()
    try:
        await callback.message.edit_text(**gen_week_homeworks_list(next_date, globals.data.student_name))
    except TelegramBadRequest as exp:
        if "message is not modified" not in exp.message:
            print("[ERROR]", exp.message)


@dp.callback_query(F.data == "tip_lesson_detail")
async def callback_week_timetable(callback: CallbackQuery):
    if check_user(callback.from_user, whitelistusers): return

    await callback.answer(text="Нажмите на кнопку с номером урока, чтобы получить его подробное описание", show_alert=True)

@dp.callback_query(F.data.startswith("lesson_detail"))
async def callback_week_timetable(callback: CallbackQuery):
    if check_user(callback.from_user, whitelistusers): return

    callback_data = callback.data.removeprefix("lesson_detail_")
    prev_msg = callback_data[:callback_data.find("_")]

    callback_data = callback_data[callback_data.find("_") + 1:]
    lesson_num = int(callback_data[:callback_data.find("_")])

    callback_data = callback_data[callback_data.find("_") + 1:]
    lesson_date = date.fromisoformat(callback_data)

    await callback.answer()
    try:
        await callback.message.edit_text(**gen_lesson_detail(lesson_date, lesson_num, prev_msg, globals.data.student_name))
    except TelegramBadRequest as exp:
        if "message is not modified" not in exp.message:
            print("[ERROR]", exp.message)


async def main():
    update_diary_interval = 10 * 60
    await globals.load_data("data.json")
    await globals.run_update_diary(update_diary_interval)
    await dp.start_polling(bot)

asyncio.run(main())
