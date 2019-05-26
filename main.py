import modules.telegram_bot as bot
import modules.weather_module as weather
import modules.database_module as database
import threading
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Set settings file and database file paths", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("settings_file", help="settings file path")
    parser.add_argument("database_file", help="database file path")
    return parser.parse_args()


def read_line(settings_file):
    return settings_file.readline().split('\n')[0]


def read_settings(settings_filename):
    with open(settings_filename, "r") as settings_file:
        bot_token = read_line(settings_file)
        weather_api_key = read_line(settings_file)
        weather_link = read_line(settings_file)
        forecast_link = read_line(settings_file)

    return bot_token, weather_api_key, weather_link, forecast_link


def run():
    args = parse_args()
    bot_token, weather_api_key, weather_link, forecast_link = read_settings(args.settings_file)
    weather.init_weather_module(weather_link, forecast_link, weather_api_key)
    bot.init_bot(bot_token)
    database.init_database_module(args.database_file)

    sub_thread = threading.Thread(target=bot.unprocessed_notifications_checker)
    sub_thread.start()

    bot.start_polling()


if __name__ == "__main__":
    run()
