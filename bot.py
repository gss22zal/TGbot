import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPERATOR_USER_ID = os.getenv("OPERATOR_USER_ID")

SERVICES = """💅 **Наши услуги:**

1️⃣ Стрижка и укладка
2️⃣ Окрашивание волос
3️⃣ Маникюр
4️⃣ Педикюр
5️⃣ Уход за лицом
6️⃣ Наращивание ресниц

Выберите интересующую услугу по номеру или запишитесь к нашему мастеру! ✨"""

COMPANY_INFO = """✨ **О салоне красоты:**

Добро пожаловать в наш салон красоты!

Мы предоставляем профессиональные услуги в области красоты и ухода с 2018 года.

✅ Опытные мастера
✅ Премиум материалы
✅ Комфортная атмосфера
✅ Индивидуальный подход

Время работы: ежедневно с 09:00 до 20:00

Контакты:
📧 salon@beauty.com
📞 +7 (999) 876-54-32"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📚 Каталог услуг", "ℹ️ О компании"],
        ["☎️ Контакты"]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    await update.message.reply_text(
        "✨ Добро пожаловать в салон красоты!\n\n"
        "Выберите интересующую вас услугу или запишитесь к мастеру 💄",
        reply_markup=reply_markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📚 Каталог услуг":
        await update.message.reply_text(SERVICES, parse_mode="Markdown")
        await update.message.reply_text(
            "Нажмите 'Записаться' чтобы забронировать место у мастера!",
            reply_markup=ReplyKeyboardMarkup(
                [["📅 Записаться"], ["🔙 Назад в меню"]],
                resize_keyboard=True
            )
        )

    elif text == "ℹ️ О компании":
        await update.message.reply_text(COMPANY_INFO, parse_mode="Markdown")

    elif text == "☎️ Контакты":
        await update.message.reply_text(
            "📧 Email: salon@beauty.com\n"
            "📞 Телефон: +7 (999) 876-54-32\n"
            "🕐 Режим работы: 09:00-20:00 (ежедневно)\n"
            "📍 Адрес: ул. Красоты, д. 42",
            reply_markup=ReplyKeyboardMarkup(
                [["📅 Записаться"], ["🔙 Назад в меню"]],
                resize_keyboard=True
            )
        )

    elif text == "📅 Записаться":
        user_id = update.message.chat_id
        user_name = update.message.from_user.first_name or "Клиент"

        try:
            await context.bot.send_message(
                chat_id=int(OPERATOR_USER_ID),
                text=f"💅 Новая запись на услугу!\n\n"
                     f"👤 Имя: {user_name}\n"
                     f"🆔 ID: {user_id}"
            )
        except Exception as e:
            print(f"Ошибка отправки сообщения мастеру: {e}")

        await update.message.reply_text(
            "📅 Спасибо! Мастер свяжется с вами в ближайшее время для уточнения деталей и времени.\n\n"
            "Ваш ID: " + str(user_id),
            reply_markup=ReplyKeyboardMarkup(
                [["🔙 Назад в меню"]],
                resize_keyboard=True
            )
        )

    elif text == "🔙 Назад в меню":
        keyboard = [
            ["📚 Каталог услуг", "ℹ️ О компании"],
            ["☎️ Контакты"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Главное меню:", reply_markup=reply_markup)

    else:
        await update.message.reply_text(
            "Пожалуйста, выберите опцию из меню ☝️"
        )


def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не установлен в .env")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
