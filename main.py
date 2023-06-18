import threading
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue
from telegram import ReplyKeyboardMarkup
from bs4 import BeautifulSoup
import pickle
import sys


all_reviews_comments = []
all_reviews = []

ALL_REVIEWS_FILENAME = 'all_reviews.pkl'
ALL_REVIEWS_COMMENTS_FILENAME = 'all_reviews_comments.pkl'

TOKEN = ''
CHAT_ID = ''


def get_reviews(url, driver):

    driver.get(url)
    time.sleep(10)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    if 'google' in url:
        searcher = 'Google'
        driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[5]/div[9]/button[2]/div[1]').click()
        driver.find_element(By.XPATH, "//button[text()='Сначала новые']").click()
        reviews = soup.find("span", {"class": "wiI7pd"})

        if reviews:
            if reviews in all_reviews_comments:
                condition = 1
                print('Information collected successfully')
                return searcher, reviews, condition

            else:
                all_reviews.append(url)
                all_reviews_comments.append(reviews)
                with open(ALL_REVIEWS_FILENAME, 'wb') as f, open(ALL_REVIEWS_COMMENTS_FILENAME, 'wb') as n:
                    pickle.dump(all_reviews, f)
                    pickle.dump(all_reviews_comments, n)
                condition = 0
                print('Information collected successfully')
                return searcher, reviews, condition

    elif 'yandex' in url:
        searcher = 'Yandex'
        driver.find_element(By.CLASS_NAME, 'rating-ranking-view').click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "[aria-label='По новизне']").click()
        time.sleep(2)
        html = driver.page_source
        time.sleep(2)
        soup = BeautifulSoup(html, "html.parser")
        time.sleep(2)
        reviews = soup.find("span", {"class": "business-review-view__body-text"})

        if reviews:
            if reviews in all_reviews_comments:
                condition = 1
                print('Information collected successfully')
                return searcher, reviews, condition

            else:
                all_reviews.append(url)
                all_reviews_comments.append(reviews)
                with open(ALL_REVIEWS_FILENAME, 'wb') as f, open(ALL_REVIEWS_COMMENTS_FILENAME, 'wb') as n:
                    pickle.dump(all_reviews, f)
                    pickle.dump(all_reviews_comments, n)
                condition = 0
                print('Information collected successfully')
                return searcher, reviews, condition

    elif '2gis' in url:
        searcher = "2Гис"
        reviews = soup.find("a", {"class": "_ayej9u3"})

        if reviews:
            if reviews in all_reviews_comments:
                condition = 1
                print('Information collected successfully')
                return searcher, reviews, condition

            elif reviews not in all_reviews_comments and url in all_reviews:
                all_reviews_comments.append(reviews)
                with open(ALL_REVIEWS_COMMENTS_FILENAME, 'wb') as n:
                    pickle.dump(all_reviews_comments, n)
                condition = 0
                print('Information collected successfully')
                return searcher, reviews, condition

            elif url not in all_reviews and reviews not in all_reviews_comments:
                all_reviews.append(url)
                all_reviews_comments.append(reviews)
                with open(ALL_REVIEWS_FILENAME, 'wb') as f, open(ALL_REVIEWS_COMMENTS_FILENAME, 'wb') as n:
                    pickle.dump(all_reviews, f)
                    pickle.dump(all_reviews_comments, n)
                condition = 0
                print('Information collected successfully')
                return searcher, reviews, condition

        else:
            reviews = soup.find("a", {"class": "_1it5ivp"})
            if reviews:
                if reviews in all_reviews_comments:
                    condition = 1
                    print('Information collected successfully')
                    return searcher, reviews, condition

                elif reviews not in all_reviews_comments and url in all_reviews:
                    all_reviews_comments.append(reviews)
                    with open(ALL_REVIEWS_COMMENTS_FILENAME, 'wb') as n:
                        pickle.dump(all_reviews_comments, n)
                    condition = 0
                    print('Information collected successfully')
                    return searcher, reviews, condition

                elif url not in all_reviews and reviews not in all_reviews_comments:
                    all_reviews.append(url)
                    all_reviews_comments.append(reviews)
                    with open(ALL_REVIEWS_FILENAME, 'wb') as f, open(ALL_REVIEWS_COMMENTS_FILENAME, 'wb') as n:
                        pickle.dump(all_reviews, f)
                        pickle.dump(all_reviews_comments, n)
                    condition = 0
                    print('Information collected successfully')
                    return searcher, reviews, condition
    driver.quit()


def before_get_and_send(update, context):
    job_queue = context.job_queue
    button = ReplyKeyboardMarkup([['/stop_parsing']], resize_keyboard=True)
    update.message.reply_text('Чтобы остановить парсинг для добавления новых ссылок нажми на кнопку', reply_markup=button)
    job = job_queue.run_repeating(get_and_send_reviews(update, context), interval=1800, context=context)
    context.chat_data['job'] = job


def get_and_send_reviews(update, context):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("headless")
    chrome_options.add_argument("--enable-javascript")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              chrome_options=chrome_options)
    for url in all_reviews:
        searcher, reviews, condition = get_reviews(url, driver)

        if condition != 1:
            if reviews:
                for review in reviews:
                    context.bot.send_message(chat_id=CHAT_ID, text=f'{searcher}:\n{review}\n\nСсылка: {url}')
                    print(review)
        print('Reviews were checked')
        print(all_reviews)
    return lambda context: get_and_send_reviews(update, context)


def stop_parsing(update, context):
    button = ReplyKeyboardMarkup([['/add_link']], resize_keyboard=True)
    update.message.reply_text('Парсинг остановлен', reply_markup=button)


def start(update, context):
    button = ReplyKeyboardMarkup([['/add_link']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Привет!', reply_markup=button)


def add_link_info(update, context):
    update.message.reply_text('Чтобы добавить ссылку просто отправь мне ее')


def add_link(update, context):
    button = ReplyKeyboardMarkup([['/parse']], resize_keyboard=True)
    link = update.message.text
    all_reviews.append(link)
    update.message.reply_text(f'Ссылка "{link}" добавлена.', reply_markup=button)
    print(all_reviews)


def error(update, context):
    print(f'Update {update} caused error {context.error}')


def main():
    global all_reviews, all_reviews_comments

    try:
        with open(ALL_REVIEWS_FILENAME, 'rb') as f, open(ALL_REVIEWS_COMMENTS_FILENAME, 'rb') as n:
            all_reviews = pickle.load(f)
            all_reviews_comments = pickle.load(n)
    except FileNotFoundError:
        all_reviews = []
        all_reviews_comments = []

    print(all_reviews)
    print(all_reviews_comments)

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, add_link))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('add_link', add_link_info))
    dp.add_handler(CommandHandler('parse', before_get_and_send, pass_job_queue=True))
    dp.add_handler(CommandHandler('stop_parsing', stop_parsing))
    dp.add_error_handler(error)

    updater.start_polling(poll_interval=0.1)

    updater.idle()


if __name__ == '__main__':
    sys.setrecursionlimit(80000)
    threading.stack_size(200000000)
    main()
