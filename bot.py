import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPERATOR_USER_ID = os.getenv("OPERATOR_USER_ID")

SERVICES_INFO = {
    "haircut": {
        "name": "✂️ Стрижка и укладка",
        "description": "Профессиональная стрижка и укладка волос от опытных мастеров. Используются только премиум средства для ухода.",
        "price": "от 800₽"
    },
    "coloring": {
        "name": "🎨 Окрашивание волос",
        "description": "Качественное окрашивание волос профессиональными красками. Консультация стилиста включена.",
        "price": "от 1500₽"
    },
    "manicure": {
        "name": "💅 Маникюр",
        "description": "Классический и аппаратный маникюр. Шеллак, гель-лак, дизайн. Индивидуальный подход к каждому клиенту.",
        "price": "от 600₽"
    },
    "pedicure": {
        "name": "👣 Педикюр",
        "description": "Профессиональный педикюр с использованием натуральных масел и кремов. Аппаратная обработка.",
        "price": "от 700₽"
    },
    "facial": {
        "name": "✨ Уход за лицом",
        "description": "Косметические процедуры для лица: чистка, пилинг, маски. Подбор средств под тип кожи.",
        "price": "от 900₽"
    },
    "lashes": {
        "name": "👁️ Наращивание ресниц",
        "description": "Наращивание ресниц с использованием материалов премиум класса. Эффект на любой вкус.",
        "price": "от 1200₽"
    }
}

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
        [InlineKeyboardButton("📚 Каталог услуг", callback_data="show_services")],
        [InlineKeyboardButton("ℹ️ О компании", callback_data="show_company")],
        [InlineKeyboardButton("☎️ Контакты", callback_data="show_contacts")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "✨ Добро пожаловать в салон красоты!\n\n"
        "Выберите интересующую вас услугу или запишитесь к мастеру 💄",
        reply_markup=reply_markup
    )


async def show_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for service_id, service_info in SERVICES_INFO.items():
        button_text = service_info["name"]
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"service_{service_id}")])

    keyboard.append([InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "💅 **Наши услуги:**\n\nВыберите услугу для подробной информации:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def show_service_detail(update: Update, context: ContextTypes.DEFAULT_TYPE, service_id: str):
    service = SERVICES_INFO.get(service_id)
    if not service:
        return

    keyboard = [
        [InlineKeyboardButton("📅 Записаться", callback_data=f"book_{service_id}")],
        [InlineKeyboardButton("🔙 Назад к услугам", callback_data="back_to_services")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = f"""
{service['name']}

📝 **Описание:**
{service['description']}

💰 **Цена:** {service['price']}
"""

    await update.callback_query.edit_message_text(
        text=message_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "back_to_menu":
        keyboard = [
            [InlineKeyboardButton("📚 Каталог услуг", callback_data="show_services")],
            [InlineKeyboardButton("ℹ️ О компании", callback_data="show_company")],
            [InlineKeyboardButton("☎️ Контакты", callback_data="show_contacts")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Главное меню:", reply_markup=reply_markup)

    elif query.data == "show_services":
        keyboard = []
        for service_id, service_info in SERVICES_INFO.items():
            button_text = service_info["name"]
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"service_{service_id}")])
        keyboard.append([InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "💅 **Наши услуги:**\n\nВыберите услугу для подробной информации:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    elif query.data == "show_company":
        keyboard = [[InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(COMPANY_INFO, reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data == "show_contacts":
        keyboard = [[InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📧 Email: salon@beauty.com\n"
            "📞 Телефон: +7 (999) 876-54-32\n"
            "🕐 Режим работы: 09:00-20:00 (ежедневно)\n"
            "📍 Адрес: ул. Красоты, д. 42",
            reply_markup=reply_markup
        )

    elif query.data.startswith("service_"):
        service_id = query.data.replace("service_", "")
        await show_service_detail(update, context, service_id)

    elif query.data == "back_to_services":
        keyboard = []
        for service_id, service_info in SERVICES_INFO.items():
            button_text = service_info["name"]
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"service_{service_id}")])
        keyboard.append([InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "💅 **Наши услуги:**\n\nВыберите услугу для подробной информации:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    elif query.data.startswith("book_"):
        service_id = query.data.replace("book_", "")
        user_id = query.from_user.id
        user_name = query.from_user.first_name or "Клиент"
        user_phone = query.from_user.username or "не указан"

        service = SERVICES_INFO.get(service_id)

        try:
            await context.bot.send_message(
                chat_id=int(OPERATOR_USER_ID),
                text=f"💅 **Новая запись на услугу!**\n\n"
                     f"📋 Услуга: {service['name']}\n"
                     f"👤 Имя: {user_name}\n"
                     f"📱 Юзернейм: @{user_phone}\n"
                     f"🆔 ID: {user_id}\n"
                     f"💰 Цена: {service['price']}",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Ошибка отправки сообщения мастеру: {e}")

        keyboard = [
            [InlineKeyboardButton("📚 Вернуться к услугам", callback_data="show_services")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"✅ **Спасибо за заявку!**\n\n"
            f"Вы записались на услугу: {service['name']}\n\n"
            f"👤 Имя: {user_name}\n"
            f"📱 Юзернейм: @{user_phone}\n\n"
            f"Мастер свяжется с вами в ближайшее время для уточнения деталей и времени визита.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📚 Каталог услуг":
        await show_services(update, context)

    elif text == "ℹ️ О компании":
        keyboard = [[InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(COMPANY_INFO, reply_markup=reply_markup, parse_mode="Markdown")

    elif text == "☎️ Контакты":
        keyboard = [[InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "📧 Email: salon@beauty.com\n"
            "📞 Телефон: +7 (999) 876-54-32\n"
            "🕐 Режим работы: 09:00-20:00 (ежедневно)\n"
            "📍 Адрес: ул. Красоты, д. 42",
            reply_markup=reply_markup
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
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
