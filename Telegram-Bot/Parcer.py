import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
from loguru import logger

BASE_URL = "https://news.un.org/ru/news"
page = 0
SLEEP = 1

LOGGING = "logs.log"
FORMAT = "{time}{level}{message}"
logger.add(LOGGING, format=FORMAT)


# Извлечение данных со страницы
@logger.catch
def get_page(page, DATE):
    info = []
    response = requests.get(BASE_URL + "?f[0]=date%3A" + DATE + f"&page={page}")
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all(
        "article",
        {"class": "node node--type-news-story node--view-mode-unnews-teaser clearfix"},
    )
    # Извлечение заголовка для одной статьи
    for ar in articles:
        title = ar.find(
            "span",
            {"class": "field field--name-title field--type-string field--label-hidden"},
        ).text
        # Извлечение даты публикации для одной статьи
        date = ar.find("time").get("datetime")[:10]
        # Извлечение ссылки для одной статьи
        link = BASE_URL[:-8] + ar.find("a").get("href")
        # Извлечение вступительного текста одной статьи
        response_one = requests.get(link)
        time.sleep(SLEEP)
        soup_one = BeautifulSoup(response_one.content, "html.parser")
        abstract = soup_one.find(
            "div", {"class": "views-field views-field-field-news-story-lead"}
        ).text
        # Извлечение полного текста одной статьи (без заголовков, источников, таблиц)
        try:
            text = ""
            text_list = soup_one.find(
                "div",
                {
                    "class": "clearfix text-formatted field field--name-field-text-column field--type-text-long field--label-hidden field__item"
                },
            ).find_all(
                ["p", "h2", "h3"]
            )  # Добавление в текст заголовков и подзаголовков самого текста
            for i in text_list:
                text += i.text + "\n"
        except AttributeError:
            text = None
        time.sleep(SLEEP)

        row = {
            "url": link,
            "title": title,
            "date": date,
            "abstract": abstract,
            "text": text,
        }
        info.append(row)
    time.sleep(SLEEP)
    if len(articles) == 0:
        return 0
    return info


# Сбор данных с сайта
def all_pages(DATE):
    infa = []
    pages = range(100)
    for page in pages:
        inf = get_page(page, DATE)
        if inf != 0:
            infa.extend(inf)
        else:
            break
    if len(infa) == 0:
        print("Новостей по данному запросу не найдено")
    else:
        df = pd.DataFrame(infa)
        # Удаляем статьи со None
        df = df.dropna()
        # Сохранение датафрейма
        return df
