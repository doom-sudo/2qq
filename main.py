from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes, CallbackContext
import telegram.error

async def button_handler(update: Update, context):
    query = update.callback_query
    try:
        await query.answer()
    except telegram.error.BadRequest:
        pass

# 🔒 Список разрешённых пользователей (замени ID на реальные)
ALLOWED_USERS = {209309861}  # Замени на свои ID

# 🔐 Функция проверки доступа
async def check_access(update: Update) -> bool:
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        if update.message:
            await update.message.reply_text("🚫 Доступ запрещён. Свяжитесь с администратором.")
        elif update.callback_query:
            await update.callback_query.message.reply_text("🚫 Доступ запрещён.")
        return False
    return True  # Если пользователь в списке, возвращаем True

# 🚀 Функция /start и при определённых словах
async def start(update: Update, context: CallbackContext):
    if update.message is None or update.message.text is None:  # Если нет текста, выходим
        return

    text = update.message.text.lower()  # Определяем text сразу
    trigger_words = ["привет", "hi", "salut", "начать", "старт"]

    # Выводим отладочную информацию
    print(f"Проверяем текст: {text}")

    if any(word in text.split() for word in trigger_words) or text.startswith("/"):
        if not await check_access(update):  # Проверяем доступ
            return  # Если доступа нет, выходим

        await update.message.reply_text("✅ Доступ разрешён. Добро пожаловать!")  # Добавляем сообщение о доступе
        keyboard = [[InlineKeyboardButton("👥 Список диспетчеров", callback_data='dispatchers')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🚛 Главное меню:", reply_markup=reply_markup)
        return  # Выход после отправки меню

        # 🚛 Если триггерные слова не сработали, ищем водителя
    driver_name = text
    drivers_info_lower = {key.lower(): value for key, value in drivers_info.items()}
    info = drivers_info_lower.get(driver_name)

    if info:
        await update.message.reply_text(info, parse_mode='HTML')

# 🔄 Главное меню (пример)
def main_menu():
    keyboard = [[InlineKeyboardButton("📋 Список водителей", callback_data='drivers')]]
    return InlineKeyboardMarkup(keyboard)

# Данные (пока вручную)
dispatchers = {
    "🚛 Диспетчер David Miller": ["Водитель Bivol Igor", "Водитель Cojocaru Victor", "Водитель Tupitcyn Anton","Водитель Joseph Garry","Водитель Feriani Mohamed","Водитель Yaser Ahmad",
                                 "Водитель Starohcotelnii Alexandr"]

}

drivers_info = {
    "Водитель Bivol Igor": (
        "📌 Driver Name: Bivol Igor \n"
        "📞 Phone Number: 704-454-8656 \n"
        "🚛 Truck Number: 02"
        "🚂 Trailer Number: 165146 \n"
        "🔑 VIN:245354353 \n" 
        "⚓Trailer Type: R \n"
        "⚖ Weight:44.000 \n"
        "🅱 Owner: da"
    ),
    "Водитель James": (
        "📌 Driver Name: James \n"
        "📞 Phone Number: 437439743 \n"
        "🚛 Truck Number:34343 \n"
        "🚂 Trailer Number:3434342 \n"
        "🔑 VIN:989774208320 \n"
        "⚓Ramps: da \n"
        "⚖ Weight: 3232 \n"
        "🅱 Owner: da"
    ),
}
# URL для фотографий и файлов
drivers_files = {
    "Водитель Chris": {
        "photo": "https://www.google.com/",
        "files": "https://www.google.com/"
    },
        "Водитель James": {
        "photo": "https://www.google.com/",
        "files": "https://www.google.com/"
    },
}

async def show_dispatchers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in dispatchers.keys()]
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data='start')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("👥 Выберите диспетчера:", reply_markup=reply_markup)


async def show_drivers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    selected_dispatcher = query.data
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in dispatchers[selected_dispatcher]]
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data='dispatchers')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(f"🚛 Водители диспетчера {selected_dispatcher}:", reply_markup=reply_markup)

async def show_driver_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    selected_driver = query.data
    keyboard = [
        [InlineKeyboardButton("📸 Фото", url=drivers_files[selected_driver]["photo"]),
         InlineKeyboardButton("📂 Файлы", url=drivers_files[selected_driver]["files"])],
        [InlineKeyboardButton("⬅️ Назад", callback_data='dispatchers')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(f"{drivers_info[selected_driver]}", reply_markup=reply_markup)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Переход по различным callback_data
    if query.data == 'start':
        await start(update, context)
    elif query.data == 'dispatchers':
        await show_dispatchers(update, context)
    elif query.data in dispatchers:
        await show_drivers(update, context)
    elif query.data in drivers_info:
        await show_driver_info(update, context)
    elif query.data.startswith("photo_"):
        selected_driver = query.data.split("_")[1]

        # Проверяем, есть ли фото для выбранного водителя
        if selected_driver in drivers_files and "photo" in drivers_files[selected_driver]:
            photo_path = drivers_files[selected_driver]["photo"]
            try:
                await query.message.reply_photo(photo=open(photo_path, 'rb'))
            except Exception as e:
                await query.message.reply_text(f"Ошибка при отправке фото: {e}")
        else:
            await query.message.reply_text("Фото не найдено для этого водителя.")
    elif query.data.startswith("files_"):
        selected_driver = query.data.split("_")[1]

        # Проверяем, есть ли документ для выбранного водителя
        if selected_driver in drivers_files and "document" in drivers_files[selected_driver]:
            file_path = drivers_files[selected_driver]["document"]
            try:
                await query.message.reply_document(document=open(file_path, 'rb'))
            except Exception as e:
                await query.message.reply_text(f"Ошибка при отправке документа: {e}")
        else:
            await query.message.reply_text("Документы не найдены для этого водителя.")


# Создание приложения
app = Application.builder().token("8101558494:AAFNh4jqCdeQFgCihkOJEpLfhJ1GE8CSupg").build()

# Добавление обработчиков
app.add_handler(CallbackQueryHandler(show_dispatchers, pattern="^dispatchers$"))
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    app.run_polling()
