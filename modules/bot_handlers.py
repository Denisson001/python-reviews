import modules.database_module as database
from modules.telegram_bot import bot
import modules.bot_functions as func
import modules.datetime_helper as helper


@bot.message_handler(commands=['start', 'help'])
def handle_start_and_help(message):
    bot.send_message(message.chat.id, 'Hello, ' + message.from_user.first_name + '! I`m the weather bot.\n' +
                     'I can help you to know the weather in any city or make a daily notification.\n' +
                     'Use command /weather to know the weather.\n' +
                     'Use command /add to make new daily notification.\n' +
                     'Use command /show to see current notifications.\n' +
                     'Use command /remove to remove notifications.')


@bot.message_handler(commands=['weather'])
def handle_weather(message):
    bot.send_message(message.chat.id, 'For what city do you want to know the weather?')
    bot.register_next_step_handler(message, send_weather)


def send_weather(message):
    func.send_weather(bot, message.chat.id, message.text)


notification_city = None
notification_time = None


@bot.message_handler(commands=['add'])
def handle_add_notification(message):
    bot.send_message(message.chat.id, 'For what city do you want to make a daily notification?')
    bot.register_next_step_handler(message, get_notification_city)


def get_notification_city(message):
    global notification_city
    notification_city = message.text
    bot.send_message(message.chat.id,
                     'For what time do you want to make a daily notification?\nUse [hh:mm] time format (without brackets).')
    bot.register_next_step_handler(message, get_notification_time)


def get_notification_time(message):
    if not helper.check_time_format(message.text):
        bot.send_message(message.chat.id, 'Wrong time format. Operation aborted.')
        return

    global notification_time
    notification_time = message.text + ':00'
    database_message = database.add_notification(message.chat.id, notification_city, notification_time)
    bot.send_message(message.chat.id, database_message)


@bot.message_handler(commands=['show'])
def handle_show_notifications(message):
    func.send_current_user_notifications(bot, message.chat.id)


@bot.message_handler(commands=['remove'])
def handle_delete_notification(message):
    notifications_count = func.send_current_user_notifications(bot, message.chat.id)
    if notifications_count:
        bot.send_message(message.chat.id,
                         'Send me notification numbers that you want to remove.\nUse spaces to separate numbers.')
        bot.register_next_step_handler(message, get_notification_numbers)


def get_notification_numbers(message):
    try:
        notification_numbers = set(map(int, message.text.split(' ')))
        database_message = database.remove_notifications(message.chat.id, notification_numbers)
        bot.send_message(message.chat.id, database_message)
    except Exception:
        bot.send_message(message.chat.id, 'Wrong input format. Operation aborted.')
