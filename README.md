<a name="readme-top"></a>

[![MIT License][license-shield]][license-url]

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
    <li><a href="#использование">Использование</a></li>
    <li><a href="#контакты">Контакты</a></li>
  </ol>
</details>



### О проекте

На данном этапе проект представляет собой парсер русскоязычной версии [новостного сайта Организации Объединённых Наций](https://news.un.org/ru).

## Технологии

Для реализации проекта использовались следующие технологии:

* [![Python][Python.org]][Python-url]
  * [![Pandas][Рandas.pydata.org]][Pandas-url]
  * [![Numpy][Numpy.org]][Numpy-url]
  * [![Matplotlib][Matplotlib.org]][Matplotlib-url]

<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>


## Начало работы

Pапустите ноутбук и последовательно выполняйте ячейки. В случае, если вы не хотите заниматься парсингом самостоятельно, можно загрузить готовый датафрейм.

На данном этапе проект состоит из двух частей:
* Часть 1.1. Реализация парсера
* Часть 1.2. Первичный анализ данных

<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>

## Использование

На данном этапе данный проект можно использовать для сбора информации с [новостого сайта ООН](https://news.un.org/ru) для дальнейшего анализа текстов. А также для визуализации и первичного анализа текстовых данных из этого источника.

Так как парсинг может занимать десятки часов, предоставляется ссылка на готовый [датафрейм](https://drive.google.com/file/d/13KoLBhEIwzeubdTehwK9ct25vvithZQf/view?usp=share_link), полученный с помощью данного парсера. Структура датафрейма:

| url | title | date | abstract | text | tag |
|----------|----------|----------|-|-|-|
| url статьи   | Заголовок статьи   | Время публикации статьи   | Вступительный текст статьи | Полный текст статьи | Рубрика| 

Датафрейм содержит данные по 30900 статьям, разбитых на десять рубрик:
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

Вы можете парсить сайт по данным тиматикам самостоятельно, регулируя количество статей для каждой тематики с помощью переменной `DEPTH`.

Вместо данных рубрик, можно самостоятельно парсить сайт по географическим регионам:
* `asia-pacific` - Азия
* `americas` - Америка
* `africa` - Африка
* `middle-east` - Ближний Восток
* `europe` - Европа


Для этого надо в цикле `# Сбор данных с сайта по рубрикам` заменить список `TOPIC` на список `REGION`, а в переменной `HOW_G` прописать `'/region/'`. Соответствующие пометки есть в коде.

<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>

## Контакты

Гандлин Александр - [Stepik](https://stepik.org/users/79694206/profile)

Ссылка на проект: [https://github.com/GandlinAlexandr/NLP_projec](https://github.com/GandlinAlexandr/NLP_projec)

<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>


[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt

[Python-url]: https://python.org/
[Python.org]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue

[Pandas-url]: https://pandas.pydata.org/
[Рandas.pydata.org]: https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white

[Numpy-url]: https://numpy.org/
[Numpy.org]: https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white

[Matplotlib-url]: https://matplotlib.org/
[Matplotlib.org]: https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black
