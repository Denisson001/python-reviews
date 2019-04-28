import modules.weather_module as weather
import modules.database_module as database


def send_weather(bot, chat_id, city):
    weather_report, image_path = weather.get_weather(city)
    bot.send_message(chat_id, weather_report)
    if image_path is not None:
        bot.send_photo(chat_id, image_path)


def send_current_user_notifications(bot, chat_id):
    database_message, notifications_count = database.get_user_notifications(chat_id)
    bot.send_message(chat_id, database_message)
    return notifications_count


def send_forecast(bot, chat_id, city, days):
    forecast_report = weather.get_forecast(city, days)
    bot.send_message(chat_id, forecast_report)
