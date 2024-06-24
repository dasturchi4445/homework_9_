import logging

import asyncpg
from aiogram import Bot, Dispatcher, types

API_TOKEN = '7361801423:AAFbDRViSXi0eq-JC4Fg8t4dfjmX2uE-NnE'  # BotFather tomonidan berilgan tokenni kiriting

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def create_db_pool():
    return await asyncpg.create_pool(dsn="postgres://username:password@localhost/mydatabase")


db_pool = None


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name

    async with db_pool.acquire() as connection:
        user = await connection.fetchrow("SELECT * FROM users WHERE user_id=$1", user_id)
        if user:
            await message.reply("Siz allaqachon ro'yxatdan o'tgansiz!")
        else:
            await connection.execute("INSERT INTO users (user_id, username, full_name) VALUES ($1, $2, $3)", user_id,
                                     username, full_name)
            await message.reply("Xush kelibsiz! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Bu bot sizga yordam beradi. /start buyrug'ini bosing va ro'yxatdan o'ting.")


async def on_startup(dp):
    global db_pool
    db_pool = await create_db_pool()


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, on_startup=on_startup)
