import telebot
import time
import modules.database_module as database
import modules.bot_functions as func

bot = None


def init_bot(token):
    global bot
    bot = telebot.TeleBot(token)
    import modules.bot_handlers


def unprocessed_notifications_checker():
    while True:
        notifications = database.get_unprocessed_notifications()
        for notification in notifications:
            func.send_weather(bot, notification[0], notification[1])
        time.sleep(55)


def start_polling():
    bot.polling()
