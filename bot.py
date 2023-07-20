import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Установка уровня логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Токен доступа к боту Telegram
TOKEN = '6369865901:AAGAiI8IMFbjbK8H28wX56NAT2lfPDiUZjU'

# Имя файла JSON с учетными данными OAuth 2.0 для доступа к Google таблице
JSON_FILE = 'cread.json'

# Имя таблицы в Google Sheets
SHEET_NAME = 'ALLAZI'

# Устанавливаем соединение с Google таблицей
credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
gc = gspread.authorize(credentials)
sheet = gc.open(SHEET_NAME).sheet1

# Функция для обработки команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот, который записывает информацию в Google таблицу. Пожалуйста, отправьте мне сообщение.")

# Функция для обработки сообщений от пользователей
def echo(update, context):
    message = update.message.text
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    
    # Записываем информацию в Google таблицу
    sheet.append_row([user_id, username, message])

    context.bot.send_message(chat_id=update.effective_chat.id, text="Сообщение успешно записано!")

# Функция для обработки ошибок
def error(update, context):
    logging.error(f'Update {update} caused error {context.error}')

# Создаем экземпляр класса Updater и передаем в него токен бота
updater = Updater(token=TOKEN, use_context=True)

# Получаем экземпляр класса Dispatcher для регистрации обработчиков
dispatcher = updater.dispatcher

# Регистрируем обработчики команд и сообщений
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

# Регистрируем обработчик ошибок
dispatcher.add_error_handler(error)

# Запускаем бота
updater.start_polling()