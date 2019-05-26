import modules.database_module as database
from modules.telegram_bot import bot
import modules.bot_functions as func
import modules.datetime_helper as helper


MAX_FORECAST_DAYS_NUMBER = 7
CITY_DICT = dict()


@bot.message_handler(commands=['start', 'help'])
def handle_start_and_help(message):
    bot.send_message(message.chat.id, 'Hello, ' + message.from_user.first_name + '! I`m the weather bot.\n' +
                     'I can help you to know the weather in any city or make a daily notification.\n' +
                     'Use command /weather to know the weather.\n' +
                     'Use command /add to make new daily notification.\n' +
                     'Use command /show to see current notifications.\n' +
                     'Use command /remove to remove notifications.\n'
                     'Use command /forecast to know weather forecast.')


@bot.message_handler(commands=['weather'])
def handle_weather(message):
    bot.send_message(message.chat.id, 'For what city do you want to know the weather?')
    bot.register_next_step_handler(message, send_weather)


def send_weather(message):
    func.send_weather(bot, message.chat.id, message.text)


@bot.message_handler(commands=['add'])
def handle_add(message):
    bot.send_message(message.chat.id, 'For what city do you want to make a daily notification?')
    bot.register_next_step_handler(message, get_notification_city)


def get_notification_city(message):
    CITY_DICT[message.chat.id] = message.text
    bot.send_message(message.chat.id,
                     'For what time do you want to make a daily notification?\n' +
                     'Use [hh:mm] time format (without brackets).')
    bot.register_next_step_handler(message, get_notification_time)


def get_notification_time(message):
    notification_city = CITY_DICT[message.chat.id]
    del CITY_DICT[message.chat.id]
    if not helper.check_time_format(message.text):
        bot.send_message(message.chat.id, 'Wrong time format. Operation aborted.')
        return
    notification_time = message.text + ':00'
    database_message = database.add_notification(message.chat.id, notification_city, notification_time)
    bot.send_message(message.chat.id, database_message)


@bot.message_handler(commands=['show'])
def handle_show(message):
    func.send_current_user_notifications(bot, message.chat.id)


@bot.message_handler(commands=['remove'])
def handle_remove(message):
    notifications_count = func.send_current_user_notifications(bot, message.chat.id)
    if notifications_count:
        bot.send_message(message.chat.id,
                         'Send me notification numbers that you want to remove.\n' +
                         'Use spaces to separate numbers.')
        bot.register_next_step_handler(message, get_notification_numbers)


def get_notification_numbers(message):
    try:
        notification_numbers = set(map(int, message.text.split(' ')))
        database_message = database.remove_notifications(message.chat.id, notification_numbers)
        bot.send_message(message.chat.id, database_message)
    except Exception:
        bot.send_message(message.chat.id, 'Wrong input format. Operation aborted.')


@bot.message_handler(commands=['forecast'])
def handle_forecast(message):
    bot.send_message(message.chat.id, 'For what city do you want to know the weather forecast?')
    bot.register_next_step_handler(message, get_forecast_city)


def get_forecast_city(message):
    CITY_DICT[message.chat.id] = message.text
    bot.send_message(message.chat.id,
                     'For how many days do you want to know the forecast.\nSend a number between 1 and ' +
                     str(MAX_FORECAST_DAYS_NUMBER) + '.')
    bot.register_next_step_handler(message, get_forecast_days_number)


def get_forecast_days_number(message):
    forecast_city = CITY_DICT[message.chat.id]
    del CITY_DICT[message.chat.id]
    try:
        forecast_days_number = int(message.text)
        if forecast_days_number <= 0 or forecast_days_number > MAX_FORECAST_DAYS_NUMBER:
            bot.send_message(message.chat.id, 'Wrong input format. Operation aborted.')
            return
    except Exception:
        bot.send_message(message.chat.id, 'Wrong input format. Operation aborted.')
        return
    func.send_forecast(bot, message.chat.id, forecast_city, forecast_days_number)
