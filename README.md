# 🏠 Rent Telegram Bot

Telegram-бот для автоматизации приема заявок на посуточную аренду объектов.

Бот помогает владельцам недвижимости получать и структурировать заявки клиентов без ручной обработки сообщений.

## 🚀 Возможности

- Клиент выбирает интересующий объект аренды
- Бот запрашивает контактные данные
- Заявка автоматически сохраняется в Google Sheets
- Владелец получает уведомление о новом клиенте
- Поддерживается отмена диалога

## 🛠 Технологии

- Python 3
- python-telegram-bot
- Google Sheets API
- gspread
- Async/Await

## 📌 Сценарий работы

1. Пользователь запускает бота командой:
   
/start

2. Выбирает объект:

3. Оставляет контактный номер.

4. Данные сохраняются:

Username | Contact | Date | Object


5. Владелец получает уведомление о новом запросе.

## ⚙️ Установка

Клонировать репозиторий:

```bash
git clone https://github.com/username/rent-telegram-bot.git
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Добавить файл:

`credentials.json` с ключами Google Service Account.

Настроить переменные:

```bash
TOKEN = "YOUR_TELEGRAM_TOKEN"
LANDLORD_ID = YOUR_CHAT_ID
```

Запуск:
`python bot.py`
