from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)
import gspread
from datetime import datetime

# ────────────────────────────────────────────────
# Настройки
# ────────────────────────────────────────────────

TOKEN = os.getenv("BOT_TOKEN")
LANDLORD_ID = int(os.getenv("LANDLORD_ID"))

# Подключение к Google Sheets (один раз при старте)
gc = gspread.service_account(filename='credentials.json')
sheet = gc.open('clients-for-rent').sheet1

# Состояния разговора
OBJECT, CONTACT = range(2)

# ────────────────────────────────────────────────
# Хендлеры
# ────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Привет! 👋\n\n"
        "Какой объект вас интересует для посуточной аренды?\n\n"
        "Напишите, пожалуйста:\n"
        "• Дом\n"
        "• Летний дом\n"
        "• Баня\n"
        "или конкретное название, если знаете"
    )
    return OBJECT


async def get_object(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_object = update.message.text.strip()

    if not selected_object:
        await update.message.reply_text(
            "Пожалуйста, напишите название или тип объекта."
        )
        return OBJECT

    # Сохраняем во временном хранилище пользователя
    context.user_data['selected_object'] = selected_object

    await update.message.reply_text(
        f"Отлично, вы выбрали: <b>{selected_object}</b>\n\n"
        "Для подтверждения брони и связи с вами пришлите, пожалуйста,\n"
        "ваш номер телефона.",
        parse_mode="HTML"
    )
    return CONTACT


async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    contact = update.message.text.strip()
    username = update.effective_user.username or 'нет username'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    selected_object = context.user_data.get('selected_object', 'не указан')

    # Запись в Google Sheets
    # Порядок колонок должен быть: Username | Контакт | Время | Выбранный объект
    row = [username, contact, timestamp, selected_object]

    try:
        sheet.append_row(row)
    except Exception as e:
        print(f"Ошибка записи в Google Sheets: {e}")

    # Сообщение арендодателю
    message = (
        f"🔔 Новый лид!\n\n"
        f"Объект: <b>{selected_object}</b>\n"
        f"Контакт: {contact}\n"
        f"Username: @{username}\n"
        f"Ссылка: https://t.me/{username if username != 'нет username' else 'нет'}\n"
        f"Время: {timestamp}"
    )

    try:
        await context.bot.send_message(
            chat_id=LANDLORD_ID,
            text=message,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Ошибка отправки арендодателю: {e}")

    # Ответ пользователю
    await update.message.reply_text(
        "Спасибо! Всё записали.\n"
        "С вами скоро свяжутся по указанному номеру."
    )

    # Очищаем временные данные
    context.user_data.clear()

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Действие отменено.")
    context.user_data.clear()
    return ConversationHandler.END


# ────────────────────────────────────────────────
# Запуск
# ────────────────────────────────────────────────

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            OBJECT:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_object)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_contact)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True,
    )

    app.add_handler(conv_handler)
    print("Бот запущен. Ожидание сообщений...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == '__main__':
    main()