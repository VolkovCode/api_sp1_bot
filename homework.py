import os
import requests
import telegram
import time
from dotenv import load_dotenv

load_dotenv()


PRACTICUM_TOKEN = os.getenv("AgAAAAAtLdfwAAYckZwe6hJ_b0W4uyGcOCYocB4")
TELEGRAM_TOKEN = os.getenv("AAFgiAgLUMMeYszzrZM-NYqg0m-pHOAZTt0")
CHAT_ID = os.getenv('319385142')
proxy = telegram.utils.request.Request(proxy_url='https://110.137.65.25:3128/') 

def parse_homework_status(homework):
    homework_name = homework['homework_name']
    if homework['status'] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    from_date = 0
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}    
    params = {'from_date': current_timestamp}
    homework_statuses = requests.get('https://praktikum.yandex.ru/api/user_api/homework_statuses/', 
                                     params=params, headers=headers)
    return homework_statuses.json()


def send_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN, request=proxy)
    return bot.send_message(chat_id=CHAT_ID, text='Привет, я ботик и у меня баги')


def main():
    current_timestamp = int(time.time())  # начальное значение timestamp

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(new_homework.get('homeworks')[0]))
            current_timestamp = new_homework.get('current_date')  # обновить timestamp
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
