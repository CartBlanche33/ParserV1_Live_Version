import requests
import time

TOKEN = "7981399325:AAGZGt-PUMjzNgIoYNo2TKZMyOyxEBN2jCA"
CHAT_ID = -1002601210164  # вставь свой chat_id
ALT_TOKEN = "7981399325:AAGZGt-PUMjzNgIoYNo2TKZMyOyxEBN2jCA"
ALT_CHAT_ID = -1002623615315

# def send_telegram_message(text):
#     url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
#     payload = {
#         "chat_id": CHAT_ID,
#         "text": text
#     }
#     try:
#         for i in range(5):
#             requests.post(url, data=payload)
#             if i < 5 - 1:
#                 time.sleep(15)
#     except Exception as e:
#         print(f"Ошибка при отправке в Telegram: {e}")


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Ошибка при отправке в Telegram: {e}")


def send_telegram_to_alt_channel(text):
    url = f"https://api.telegram.org/bot{ALT_TOKEN}/sendMessage"
    payload = {
        "chat_id": ALT_CHAT_ID,
        "text": text
    }
    requests.post(url, data=payload)


# Cucu = "test"
# send_mesaj = send_telegram_to_alt_channel(Cucu)
