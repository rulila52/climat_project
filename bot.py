from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Настройка логгирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Функция для чтения пороговой температуры из файла
def read_threshold():
    with open("threshold_temperature.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            threshold = line.strip()
            threshold_temperature = float(threshold)
        return threshold_temperature

# Функция для записи пороговой температуры в файл
def write_threshold(threshold):
    with open("threshold_temperature.txt", "w") as file:
        file.write(str(threshold))

# Функция для чтения текущей температуры из файла
def read_current_temperature():
    try:
        with open("current_temperature.txt", "r") as file:
            current_temperature = file.read().strip()
            return (current_temperature + " градусов Цельсия") if current_temperature else "Текущее значение неизвестно"
    except FileNotFoundError:
        return "Файл с текущей температурой не найден"

# Обработчик команды /set_threshold
def set_threshold(update, context):
    text = update.message.text
    threshold = float(text.split(" ")[1])
    write_threshold(threshold)
    update.message.reply_text(f'Пороговая температура установлена: {threshold} градусов Цельсия')

# Обработчик команды /get_threshold
def get_threshold(update, context):
    threshold_temperature = read_threshold()
    update.message.reply_text(f'Ваша пороговая температура: {threshold_temperature} градусов Цельсия')

# Обработчик команды /current_temperature
def get_current_temperature(update, context):
    current_temperature = read_current_temperature()
    update.message.reply_text(f'Текущая температура: {current_temperature}')

# Функция для обработки всех прочих сообщений
def echo(update, context):
    update.message.reply_text('Неизвестная команда!')

def main():
    # Инициализация токена бота
    updater = Updater("6769840989:AAEHvccx6C_3_dhRwn-KssOb_PixGtQWAKs")

    # Получение диспетчера для регистрации обработчиков
    dp = updater.dispatcher

    # Чтение пороговой температуры из файла
    threshold_temperature = read_threshold()

    # Регистрация обработчиков команд
    dp.add_handler(CommandHandler("set_threshold", set_threshold))
    dp.add_handler(CommandHandler("get_threshold", get_threshold))
    dp.add_handler(CommandHandler("current_temperature", get_current_temperature))

    # Регистрация обработчика для всех прочих сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запуск бота
    updater.start_polling()

    print('Bot started!')

    # Бот работает до нажатия Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
