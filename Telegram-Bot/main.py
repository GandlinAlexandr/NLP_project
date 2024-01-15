import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import os
import Parcer
import Preprocessing_ML_hist
import pandas as pd
from aiogram.types import FSInputFile
import matplotlib.pyplot as plt
from aiogram.utils.markdown import hlink
from dotenv import load_dotenv

load_dotenv()

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Бот
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()

df_for_ML = pd.read_pickle("df_regions_clean_for_model.p", compression="gzip")
Log_Tf_Idf = Preprocessing_ML_hist.LogR(df_for_ML)


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Пожалуйста, введите дату в формате ДД.ММ.ГГГГ или ММ.ГГГГ "
        "(например, '29.03.2021' или '03.2021'). "
        "И, если хотите, задайте произвольную тему через пробел от даты. "
        "Например: '29.03.2021 Изменение климата'."
    )


# Хэндлер на команду /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.reply(
        "Пользоваться ботом просто. Он принимает дату, "
        "написанную в формате ДД.ММ.ГГГГ или ММ.ГГГГ (например, '29.03.2021' или "
        "'03.2023') и выдаёт график "
        "распределения статей по регионам мира за данную дату.\n\nПомимо этого через пробел от даты "
        "можно ввести произвольное описание темы (например, '29.03.2023 Изменение климата') "
        "и бот помимо графика выдаст наиболее близкую по теме "
        "статью за указанную дату.\n\n"
        "PS: запрос статей за месяц обрабатывается несколько минут. "
        "В зависимости от количества статей в этом месяце."
    )


# Хэндлер на сообщение
@dp.message()
async def echo_message(message: types.Message):
    await message.answer("Прогнозирование - дело тонкое. Пожалуйста, подождите ⌚")
    text = message.text
    theme = " ".join(text.split(" ")[1::])
    DATE = "-".join(text.split(" ")[0].split(".")[::-1])
    try:
        df = Parcer.all_pages(DATE)
        df = Preprocessing_ML_hist.prep(df)
        df_with_predict = Preprocessing_ML_hist.predict(df, Log_Tf_Idf)
        hist = Preprocessing_ML_hist.hist(df_with_predict, DATE)
        plt.savefig("foo.png")
        hist = FSInputFile("foo.png")
        await message.reply_photo(hist)
        index = Preprocessing_ML_hist.cosine_sim(df_with_predict, theme)[0]
        percent = Preprocessing_ML_hist.cosine_sim(df_with_predict, theme)[1]
        article = df_with_predict["url"].loc[index]
        if len(theme) > 0:
            article_link = hlink(df_with_predict["title"].loc[index], article)
            await message.reply(
                "Ваш тематический запрос:"
                + "\n"
                + theme
                + "\n\n"
                + "Самая близкая статья по теме:"
                + "\n"
                + article_link
                + "\n\n"
                + "Регион:"
                + "\n"
                + df_with_predict["regions"].loc[index]
                + "\n\n"
                + "Процент сходства:"
                + "\n"
                + percent
                + "\n\n"
                + "Дата публикации:"
                + "\n"
                + ".".join(df_with_predict["date"].loc[index].split("-")[::-1]),
                parse_mode="HTML",
            )
    except:
        await message.reply(
            "Статей по данной дате не найдено, или введён неверный запрос"
        )


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
