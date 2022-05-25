import logging
import sqlite3

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

TOKEN = '5135181457:AAEgmREifprqRrNi1rfRh9SaSB-YwuHri3k'
ADMIN = 519340190

kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(types.InlineKeyboardButton(text="Сервис PARTNER"))
kb.add(types.InlineKeyboardButton(text="Зарегистрироваться водителем такси"))
kb.add(types.InlineKeyboardButton(text="Зарегистрироваться курьером"))
kb.add(types.InlineKeyboardButton(text="Поддержка"))
kb.add(types.InlineKeyboardButton(text="АКЦИИ"))
kb.add(types.InlineKeyboardButton(text="РОЗЫГРЫШИ"))
kb.add()
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

conn = sqlite3.connect('db.db')
cur = conn.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS users(user_id INTEGER, block INTEGER);""")
conn.commit()


class dialog(StatesGroup):
    spam = State()


blacklist = State()
whitelist = State()


@dp.message_handler(commands=['start'])
async def start(message):
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = cur.fetchone()
    if message.from_user.id == ADMIN:

        await message.answer(
            'От регистрации до возможности зарабатывать 5 минут.\n'
            'Чтобы начать, нажмите\n'
            'СТАРТ\n'
            '👇👇👇👇👇👇👇👇\n'
            '\n'
            'Используйте /off чтобы приостановить подписку.',
            reply_markup=kb)
        await message.answer(
            'Хотите создать своего бота?\n'
            'Вам сюда: @Manybot\n',
            reply_markup=kb)
    else:
        if result is None:
            cur = conn.cursor()
            cur.execute(
                f'''SELECT * FROM users WHERE (user_id="{message.from_user.id}")''')
            entry = cur.fetchone()
            if entry is None:
                cur.execute(
                    f'''INSERT INTO users VALUES ('{message.from_user.id}', '0')''')
                conn.commit()
                await message.answer('')
        else:
            await message.answer('Ты был заблокирован!')


@dp.message_handler(content_types=['text'])
async def bot_message(message):
    if message.chat.type == 'private':
        if message.text == "Сервис PARTNER":
            await bot.send_message(
                message.chat.id,
                'Условия пользования\n'
                'https://telegra.ph/PARTNER-REGISTRACIYA-V-SERVISE-05-16')
        elif message.text == "Зарегистрироваться водителем такси":
            # kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # item1 = types.InlineKeyboardButton(text="ЛИЧНЫЕ ДАННЫЕ")
            # item7 = types.InlineKeyboardButton(text="ДАННЫЕ АВТОМОБИЛЯ")
            # back = types.InlineKeyboardButton(text="НАЗАД")
            # kb.add(item1, item2, back)
            await bot.send_message(message.chat.id,
                                   "Если вы хотите зарегистрироваться водителем такси,в нашем сервисе PARTNER, вам необходимо отправить БОТУ ЛИЧНЫЕ ДАННЫЕ и информацию о вашем автомобиле")
        elif message.text == "Зарегистрироваться курьером":
            await bot.send_message(message.chat.id,
                                   "Вы хотите выполнять заказы с автомобилем или без?")
        elif message.text == "Поддержка":
            await bot.send_message(message.chat.id,
                                   "Если у вас остались остались вопросы, можете отправить их в ПОДДЕРЖКУ")
        elif message.text == "АКЦИИ":
            await bot.send_message(message.chat.id,
                                   "Здесь будут все актуальные акции и скидки в сервисе")
        else:
            await bot.send_message(message.chat.id,
                                   "Здесь будут все проходящие розыгрыши")





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
