import modules.telegram_bot as bot
import modules.weather_module as weather
import modules.database_module as database
import threading


def read_settings():
    with open("settings.txt", "r") as settings_file:
        bot_token = settings_file.readline().split('\n')[0]
        weather_api_key = settings_file.readline().split('\n')[0]

    return bot_token, weather_api_key


def run():
    bot_token, weather_api_key = read_settings()
    weather.init_weather_module(weather_api_key)
    bot.init_bot(bot_token)
    database.init_database_module()

    sub_thread = threading.Thread(target=bot.unprocessed_notifications_checker)
    sub_thread.start()

    bot.start_polling()


if __name__ == "__main__":
    run()

