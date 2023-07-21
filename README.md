# MapsReviewsBot
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat-square&logo=Selenium&logoColor=white)](https://www.selenium.com/)


Бот-парсер для отслеживания новых отзывов для установленных организаций на YandexMaps, 2ГИС, GoogleMaps.
Бот позволяет загрузить необходимые организации, в которых нужно отслеживать появление новых отзывов, а затем уведомляет об их появлении в Telegram.

## Подготовка и запуск проекта
### Склонируйте репозиторий:
```
git clone https://github.com/hive937/maps_reviews_bot
```
* Установите зависимости
```
pip install -r requirements.txt
```
* Запустите бота
```
python main.py
```

## Для успешной работы проекта
Необходимо подставить в код main2.py:
- В значение TOKEN подставить токен бота, полученный в BotFather
- В значение CHAT_ID подставить id чата, в который будут присылаться уведомления


# Использованные технологии:
- Selenium
- Python-telegram-bot
- BeautifulSoup
- Telegram API

## Автор проекта
Павел Вервейн | [hive937](https://github.com/hive937)
