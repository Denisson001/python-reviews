import requests
import json

key = None


def init_weather_module(api_key):
    global key
    key = api_key


class MessageManager:
    def __init__(self):
        self.messages = list()

    def add_message(self, message_title, *message_body):
        message = list()
        message.append(message_title)
        for item in message_body:
            message.append(str(item))
        self.messages.append(message)

    def add_empty_line(self):
        self.messages.append(list())

    def get_report(self):
        report = list()
        for message in self.messages:
            if len(message):
                message[0] += ': '
            message.append('\n')
            report.append(''.join(message))
        return ''.join(report)


def make_weather_report(data):
    message_manager = MessageManager()
    message_manager.add_message('City', data['location']['name'], ', ', data['location']['country'])
    message_manager.add_message('Local time', data['location']['localtime'])
    message_manager.add_message('Temperature', data['current']['temp_c'], chr(176), 'C')
    message_manager.add_message('Feels like', data['current']['feelslike_c'], chr(176), 'C')
    message_manager.add_message('Wind speed', round(data['current']['wind_mph'] / 3.6, 1), ' mps')
    message_manager.add_message('Humidity', data['current']['humidity'], '%')
    message_manager.add_message('Pressure', round(data['current']['pressure_mb'] * 3 / 4), ' mmHg')
    return message_manager.get_report()


def get_image_path(data):
    image_path = data['current']['condition']['icon']
    return image_path[2:len(image_path)]


def get_weather(city):
    try:
        response = requests.get('http://api.apixu.com/v1/current.json', params={'key': key, 'q': city}, timeout=(2.5, 2.5))
    except Exception:
        return 'Weather api error', None

    if response.status_code != requests.codes.ok:
        return 'Bad request', None

    json_response = json.loads(response.text)
    return make_weather_report(json_response), get_image_path(json_response)


def make_forecast_report(data):
    message_manager = MessageManager()
    message_manager.add_message('City', data['location']['name'], ', ', data['location']['country'])
    message_manager.add_empty_line()
    data = data['forecast']['forecastday']

    for day_number in range(len(data)):
        message_manager.add_message(data[day_number]['date'], data[day_number]['day']['condition']['text'])
        message_manager.add_message('Minimum temperature', data[day_number]['day']['mintemp_c'], chr(176), 'C')
        message_manager.add_message('Maximum temperature', data[day_number]['day']['maxtemp_c'], chr(176), 'C')
        message_manager.add_message('Maximum wind speed', round(data[day_number]['day']['maxwind_mph'] / 3.6, 1), ' mps')
        message_manager.add_message('Total precipitation', data[day_number]['day']['totalprecip_mm'], ' mm')
        message_manager.add_empty_line()

    return message_manager.get_report()


def get_forecast(city, days):
    try:
        response = requests.get('http://api.apixu.com/v1/forecast.json', params={'key': key, 'q': city, 'days': days}, timeout=(2.5, 2.5))
    except Exception:
        return 'Weather api error'

    if response.status_code != requests.codes.ok:
        return 'Bad request'

    json_response = json.loads(response.text)
    return make_forecast_report(json_response)
