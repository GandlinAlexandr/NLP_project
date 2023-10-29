<a name="readme-top"></a>


[![MIT License][license-shield]][license-url]
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[!['Black'](https://img.shields.io/badge/code_style-black-black?style=for-the-badge)](https://github.com/psf/black)

  <h1 align="center">NLP-project</h1>

  <p align="center">
    Не судите строго, это мой первый проект
  </p>


<details>
  <summary>Содержание</summary>
  <ol>
    <li>
      <a href="#о-проекте">О проекте</a>
      <ul>
        <li><a href="#технологии">Технологии</a></li>
      </ul>
    </li>
    <li>
      <a href="#начало-работы">Начало работы</a>
    </li>
    <ul>
    <li><a href="#сбор-данных">Сбор данных</a></li>
    <ul><li><a href="#реализация-парсера">Реализация парсера</a></li></ul>
        <ul><li><a href="#первичный-анализ-данных">Первичный анализ данных</a></li></ul></ul>
    <ul><li><a href="#векторизация-текста-и-построение-моделей">Векторизация такста и построение моделей</a></li></ul><ul>
    <ul><li><a href="#предобработка-текста">Предобработка текста</a></li></ul>
    <ul><li><a href="#построение-моделей">Построение моделей</a></li></ul>
    </ul>
    <li><a href="#использование">Использование</a></li>
    <li><a href="#лицензия">Лицензия</a></li>
    <li><a href="#контакты">Контакты</a></li>
  </ol>
</details>



### О проекте

На данном этапе проект представляет собой парсер русскоязычной версии [новостного сайта Организации Объединённых Наций](https://news.un.org/ru).

## Технологии

Для реализации проекта использовались следующие технологии:

* [![Colab][Colab]][Colab-url]
* [![Kaggle][Kaggle]][Kaggle-url]
* [![Python][Python.org]][Python-url]
  * [![Matplotlib][Matplotlib.org]][Matplotlib-url]
  * [![Numpy][Numpy.org]][Numpy-url]
  * [![Pandas][Рandas.pydata.org]][Pandas-url]
  * [![scikit-learn][scikit-learn]][scikit-learn-url]

<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>

## Начало работы

Запустите ноутбук и последовательно выполняйте ячейки.

На данном этапе проект состоит из двух частей:
* Часть 1. Сбор данных
  * Реализация парсера
  * Первичный анализ данных
  * Выводы
* Часть 2. Векторизация текста и построение моделей
  * Предобработка текста
    * Word2Vec
      * Подход с Tf-Idf
      * Подход с усреднением векторов
  * Логистическая регрессия
  * Метод опорных векторов SVM
  * Наивный байесовский метод
  * Выводы

В репозитории имеется два файла: один работает со статьями, разбитыми по темам (`UN_project_topics.ipynb`), а другой работает со статьями, разбитыми по регионам (`UN_project_regions.ipynb`). 

**!!!Наилучшие модели получились для данных по регионам**. 
Поэтому файл по топикам и соотвествующий датафрейм можно игнорировать - ничего не потеряете. Я добавил его, так как кучу времени на него убил и он меня кое-чему все-таки научил.

### Сбор данных
#### Реализация парсера
Так как парсинг может занимать десятки часов, предоставляется ссылка на готовые датафреймы по [тематике](https://drive.google.com/file/d/13KoLBhEIwzeubdTehwK9ct25vvithZQf/view?usp=share_link) (открыать в `UN_project_topics.ipynb` - вот [версия датафрейма](https://drive.google.com/file/d/1uHOhshi19zbu5tHdxE0bGXM_MOa39bs9/view?usp=drive_link) с обработанным текстом) и по [регионам](https://drive.google.com/file/d/1YNy0SBSPVAn9uE8Ah6d8VkWOGauxjcyq/view?usp=drive_link) (открывать в `UN_project_regions.ipynb` - вот [версия датафрейма](https://drive.google.com/file/d/1hM3IW8FzhQw_5Iz-gPCguN4KiI8bOL7j/view?usp=drive_link) с обработанным текстом), полученные с помощью данных парсеров. Структура датафреймов в общем виде:

| url | title | date | abstract | text | topics / regions |
|----------|----------|----------|-|-|-|
| url статьи   | Заголовок статьи   | Время публикации статьи   | Вступительный текст статьи | Основной текст статьи | Рубрика или регион| 

Датафрейм по тематикам содержит данные по 22065 статьям, разбитым на десять рубрик:
* `humanitarian-aid` - Гуманитарная помощь
* `women` - Женщины
* `health` - Здравоохраниение
* `climate-change` - Климат и окружающая среда
* `culture-and-education` - Культура и образование
* `law-and-crime-prevention` - Международное право
* `peace-and-security` - Мир и безопасность
* `un-affairs` - Генеральный секретарь ООН
* `human-rights` - Права человека
* `economic-development` - Экономическое развитие

Датафрейм по регионам содержит данные по 18441 статьям и имеет следующие категории:
* `asia-pacific` - Азия
* `americas` - Америка
* `africa` - Африка
* `middle-east` - Ближний Восток
* `europe` - Европа

#### Первичный анализ данных

Представляет собой первичный анализ текстовых данных:
- Распределение категорий
- Распределение времени новостей
- Распределение по длине заголовка
- Распределение по длине вступительного текста
- Распределение по длине основного текста
- Ключевые слова по каждой из тематик

### Векторизация текста и построение моделей

#### Предобработка текста
Включает предобработку текста:
- Cегментация 
- Токенизация
- Лемматизация

Также раздел включает вектризацию текста с помощью **Word2Vect**. Использованы два способа для получения векторв для предложений:
- Усреднение векторов слов
- Взвешивание векторов слов на основе Tf-Idf


#### Построение моделей
Были использованы следующие модели для решения задачи классификации текстов:
- Логистическая регрессия
- Метод опорных векторов
- Наивный байесовский метод


<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>

## Использование

На данном этапе данный проект можно использовать для сбора информации с [новостого сайта ООН](https://news.un.org/ru) для дальнейшего анализа текстов. А также для визуализации и первичного анализа текстовых данных из этого источника.


<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>

## Лицензия

Распространяется по лицензии MIT. Дополнительную информацию см. в файле `LICENSE`.

<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>

## Контакты

Гандлин Александр - [Stepik](https://stepik.org/users/79694206/profile)

Ссылка на проект: [https://github.com/GandlinAlexandr/NLP_projec](https://github.com/GandlinAlexandr/NLP_projec)

<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>


[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/GandlinAlexandr/NLP_project/blob/main/LICENSE

[Python-url]: https://python.org/
[Python.org]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue

[Pandas-url]: https://pandas.pydata.org/
[Рandas.pydata.org]: https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white

[Numpy-url]: https://numpy.org/
[Numpy.org]: https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white

[Matplotlib-url]: https://matplotlib.org/
[Matplotlib.org]: https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black

[Colab-url]: https://colab.research.google.com/
[Colab]: https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&color=525252

[Kaggle-url]: https://www.kaggle.com/
[Kaggle]: https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=Kaggle&logoColor=white

[scikit-learn-url]: https://scikit-learn.org/
[scikit-learn]: https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white
