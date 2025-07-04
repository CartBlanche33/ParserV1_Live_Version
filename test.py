import requests

# Вставь сюда свой токен и ID чата
TOKEN = "7981399325:AAGZGt-PUMjzNgIoYNo2TKZMyOyxEBN2jCA"
CHAT_ID = -1002601210164  # вставь свой chat_id  # про это ниже объясню

# Текст, который отправим
TEXT = 'Привет! Это тестовое сообщение от моего бота 🚀'

# Отправка запроса
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
payload = {
    'chat_id': CHAT_ID,
    'text': TEXT
}

response = requests.post(url, data=payload)

# Проверка результата
if response.status_code == 200:
    print("✅ Сообщение успешно отправлено!")
else:
    print("❌ Ошибка при отправке:", response.text)
