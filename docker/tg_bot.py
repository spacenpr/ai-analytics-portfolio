import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования (чтобы видеть ошибки в `docker logs`)
logging.basicConfig(level=logging.INFO)

# Твой новый токен (я его вставил)
TELEGRAM_TOKEN = "8732007860:AAGFA_r_McliGu25saG8GE0DOicpzzA0Q0c"

# --- Хендлер для /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Анализ данных", callback_data="analyze")],
        [InlineKeyboardButton("📈 Отчет", callback_data="report")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я аналитический бот 🤖\n\n"
        "Выбери действие:",
        reply_markup=reply_markup
    )

# --- Хендлер для нажатий на кнопки ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Обязательно, чтобы Telegram убрал "часики"

    if query.data == "analyze":
        await query.edit_message_text(
            "📊 **Анализ данных:**\n"
            "• Продажи по категориям\n"
            "• A/B тесты (p-value, CI)\n"
            "• ABC-анализ товаров\n\n"
            "Для полного отчета нажми «Отчет»."
        )
    elif query.data == "report":
        await query.edit_message_text(
            "📈 **Отчет готов!**\n"
            "Выручка: 1 250 000 ₽\n"
            "Конверсия (A/B тест): +2.24% (p-value=0.03)\n"
            "Топ-товары: Ноутбук, Смартфон, Планшет\n\n"
            "Посмотреть детали: [ссылка на портфолио]"
        )
    elif query.data == "help":
        await query.edit_message_text(
            "ℹ️ **Помощь**\n\n"
            "Команды:\n"
            "/start — Главное меню\n"
            "/report — Свежий отчет\n"
            "/help — Эта справка\n\n"
            "Бот работает внутри Docker-контейнера 🐳"
        )
    elif query.data == "inline_help":
        await query.edit_message_text("Доп. справка: все команды — через /help")

# --- Хендлер для /report (команда) ---
async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 **Сводный отчет за период:**\n"
        "Выручка: 1 250 000 ₽\n"
        "Конверсия (A/B тест): +2.24% (p-value=0.03)\n"
        "Топ-товары: Ноутбук, Смартфон, Планшет"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Команды:\n"
        "/start — Главное меню\n"
        "/report — Свежий отчет\n"
        "/help — Эта справка"
    )

# --- Запуск бота ---
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", report_command))
    app.add_handler(CommandHandler("help", help_command))

    # Обработчик нажатий на кнопки
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Бот запущен в Docker-контейнере и готов к работе!")
    print("Ожидание сообщений...")

    app.run_polling()

if __name__ == "__main__":
    main()