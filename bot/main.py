import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import os
from dotenv import load_dotenv
load_dotenv()
from aiogram.types import FSInputFile

import Parcer
import Preprocessing_ML_hist
import pandas as pd
import cloudpickle
import pickle
import joblib

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Бот
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

# Хэндлер на команду /test2
@dp.message(Command("test2"))
async def cmd_test2(message: types.Message):
    await message.reply("Test 2")

# Хэндлер на сообщение
@dp.message()
async def echo_message(message:types.Message):
    text = message.text
    DATE = '-'.join(text.split(' ')[0].split('.')[::-1])
    df = pd.read_pickle('df_regions.p', compression='gzip')
    df['regions'] = ['europe', 'europe', 'asia-pacific', 'europe', 'europe', 'europe', 'europe', 'europe', 'europe',
                     'europe']
    df = Preprocessing_ML_hist.prep(df)
    x_text = df.text_clean.str.split()
    Log_Tf_Idf = cloudpickle.load(open('Log_Tf_Idf.pkl', 'rb'))
    #Log_Tf_Idf = Preprocessing_ML_hist.LogR(df)
    s = Log_Tf_Idf.predict(x_text)
    await message.answer(DATE)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
