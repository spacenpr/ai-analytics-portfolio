import requests
import json
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ================================================================
# НАСТРОЙКИ
# ================================================================
TELEGRAM_TOKEN = "8137621963:AAFsJYxJXGl8Xhcs6g8qh7-ZFl3COkIzcnk"  # Вставь свой токен!
API_URL = "http://127.0.0.1:8000/predict"

print("=" * 60)
print("🤖 TELEGRAM-БОТ ДЛЯ ПРОГНОЗА ОТТОКА")
print("=" * 60)


# ----------------------------------------------------------------
# КНОПКИ
# ----------------------------------------------------------------
def get_keyboard():
    keyboard = [
        [KeyboardButton("📊 Прогноз для тестового клиента")],
        [KeyboardButton("❓ Помощь"), KeyboardButton("ℹ️ О боте")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ----------------------------------------------------------------
# ОБРАБОТЧИКИ КОМАНД
# ----------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственное сообщение"""
    await update.message.reply_text(
        "🤖 **Банковский AI-агент**\n\n"
        "Я предсказываю, уйдет клиент из банка или нет.\n\n"
        "**Что я умею:**\n"
        "✅ Прогноз для одного клиента\n"
        "✅ Оценка риска (Высокий/Средний/Низкий)\n"
        "✅ Рекомендации по удержанию\n\n"
        "**Как использовать:**\n"
        "• Нажми кнопку 'Прогноз для тестового клиента'\n"
        "• Или отправь данные в формате JSON\n\n"
        "**Пример команды:**\n"
        "`/predict 650 35 50000 30000 2 2 3 30 0.25 Male 1 1 Standard Bronze Medium Professional Medium 2`\n\n"
        "Или просто нажми кнопку ниже! 👇",
        parse_mode='Markdown',
        reply_markup=get_keyboard()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Помощь"""
    await update.message.reply_text(
        "📚 **Помощь**\n\n"
        "**Команды:**\n"
        "/start — запустить бота\n"
        "/help — показать помощь\n"
        "/info — информация о боте\n"
        "/predict — сделать прогноз (с параметрами)\n\n"
        "**Или просто нажми кнопку 'Прогноз'** — я покажу пример с тестовыми данными.",
        parse_mode='Markdown'
    )


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Информация о боте"""
    await update.message.reply_text(
        "ℹ️ **О боте**\n\n"
        "Версия: 1.0.0\n"
        "Модель: CatBoost\n"
        "ROC-AUC: 0.856\n\n"
        "**Технологии:**\n"
        "• FastAPI (бэкенд)\n"
        "• CatBoost (ML модель)\n"
        "• Telegram Bot API\n\n"
        "**Автор:** AI Agent Developer",
        parse_mode='Markdown'
    )


async def test_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Тестовый прогноз с демо-данными"""
    await update.message.reply_text("🔮 Делаю прогноз для тестового клиента...\n\n⏳ Пожалуйста, подождите...")

    # Тестовые данные клиента с высоким риском
    test_client = {
        "credit_sco": 580,
        "age": 25,
        "balance": 10000,
        "monthly_ir": 15000,
        "tenure_ye": 1,
        "nums_card": 1,
        "nums_service": 2,
        "engagement_score": 12,
        "risk_score": 0.55,
        "gender": "Male",
        "married": 0,
        "active_member": 1,
        "customer_segment": "Mass",
        "loyalty_level": "Bronze",
        "digital_behavior": "Low",
        "occupation": "Student",
        "risk_segment": "High",
        "cluster_group": 1
    }

    try:
        response = requests.post(API_URL, json=test_client, timeout=30)

        if response.status_code == 200:
            result = response.json()

            # Эмодзи для уровня риска
            if result['risk_level'] == "Высокий":
                risk_emoji = "🔴"
            elif result['risk_level'] == "Средний":
                risk_emoji = "🟡"
            else:
                risk_emoji = "🟢"

            # Эмодзи для прогноза
            if result['churn_prediction'] == 1:
                churn_emoji = "⚠️ УЙДЕТ"
            else:
                churn_emoji = "✅ ОСТАНЕТСЯ"

            message = f"""
📊 **РЕЗУЛЬТАТ ПРОГНОЗА (тестовый клиент)**

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 **Прогноз:** {churn_emoji}
📈 **Вероятность ухода:** {result['churn_probability'] * 100:.1f}%

{risk_emoji} **Уровень риска:** {result['risk_level']}

💡 **Рекомендация:** {result['recommendation']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 **Данные клиента:**
• Возраст: 25 лет
• Баланс: 10,000 руб.
• Кредитный скор: 580
• Стаж в банке: 1 год
• Сегмент: Mass
• Уровень лояльности: Bronze
"""
            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"❌ Ошибка API: {response.status_code}")

    except requests.exceptions.ConnectionError:
        await update.message.reply_text(
            "❌ **Ошибка подключения!**\n\n"
            "Убедись, что запущен API сервер:\n"
            "```bash\npython model_api.py\n```",
            parse_mode='Markdown'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")


async def manual_predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ручной ввод данных через команду /predict"""
    args = context.args

    if len(args) < 18:
        await update.message.reply_text(
            "❌ **Недостаточно параметров!**\n\n"
            "Пример использования:\n"
            "`/predict 650 35 50000 30000 2 2 3 30 0.25 Male 1 1 Standard Bronze Medium Professional Medium 2`\n\n"
            "**Параметры (18 штук):**\n"
            "1. credit_sco — кредитный скор\n"
            "2. age — возраст\n"
            "3. balance — баланс\n"
            "4. monthly_ir — ежемесячный доход\n"
            "5. tenure_ye — лет в банке\n"
            "6. nums_card — количество карт\n"
            "7. nums_service — количество услуг\n"
            "8. engagement_score — вовлеченность (0-100)\n"
            "9. risk_score — риск (0-1)\n"
            "10. gender — Male/Female\n"
            "11. married — 0/1\n"
            "12. active_member — 0/1\n"
            "13. customer_segment — Standard/Premium/Mass/Emerging\n"
            "14. loyalty_level — Bronze/Silver/Gold\n"
            "15. digital_behavior — Low/Medium/High\n"
            "16. occupation — Professional/Manager/Student/Retired\n"
            "17. risk_segment — Low/Medium/High\n"
            "18. cluster_group — 1/2/3/4",
            parse_mode='Markdown'
        )
        return

    try:
        client_data = {
            "credit_sco": float(args[0]),
            "age": int(args[1]),
            "balance": float(args[2]),
            "monthly_ir": float(args[3]),
            "tenure_ye": int(args[4]),
            "nums_card": int(args[5]),
            "nums_service": int(args[6]),
            "engagement_score": float(args[7]),
            "risk_score": float(args[8]),
            "gender": args[9],
            "married": int(args[10]),
            "active_member": int(args[11]),
            "customer_segment": args[12],
            "loyalty_level": args[13],
            "digital_behavior": args[14],
            "occupation": args[15],
            "risk_segment": args[16],
            "cluster_group": int(args[17])
        }

        await update.message.reply_text("🔮 Делаю прогноз...")

        response = requests.post(API_URL, json=client_data, timeout=30)

        if response.status_code == 200:
            result = response.json()

            if result['risk_level'] == "Высокий":
                risk_emoji = "🔴"
            elif result['risk_level'] == "Средний":
                risk_emoji = "🟡"
            else:
                risk_emoji = "🟢"

            if result['churn_prediction'] == 1:
                churn_emoji = "⚠️ УЙДЕТ"
            else:
                churn_emoji = "✅ ОСТАНЕТСЯ"

            message = f"""
📊 **РЕЗУЛЬТАТ ПРОГНОЗА**

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 **Прогноз:** {churn_emoji}
📈 **Вероятность ухода:** {result['churn_probability'] * 100:.1f}%

{risk_emoji} **Уровень риска:** {result['risk_level']}

💡 **Рекомендация:** {result['recommendation']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"❌ Ошибка API: {response.status_code}")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений (кнопок)"""
    text = update.message.text

    if text == "📊 Прогноз для тестового клиента":
        await test_prediction(update, context)
    elif text == "❓ Помощь":
        await help_command(update, context)
    elif text == "ℹ️ О боте":
        await info_command(update, context)
    else:
        await update.message.reply_text(
            "❓ Неизвестная команда\n\n"
            "Используй кнопки меню или /help для списка команд"
        )


# ----------------------------------------------------------------
# ЗАПУСК
# ----------------------------------------------------------------
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрируем команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("predict", manual_predict))

    # Регистрируем обработчик сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Telegram-бот запущен!")
    print(f"🤖 Бот доступен: https://t.me/ваш_username_бота")
    print("Нажми Ctrl+C для остановки")

    app.run_polling()


if __name__ == "__main__":
    main()