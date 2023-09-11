import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import requests

load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')
API_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&&appid={}'

app = Flask(__name__)
app.config['DEBUG'] = True

def degToCompass(num):
    val = int((num / 22.5) + .5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        city = request.form['city']
        weather = getWeather(city)
    else:
        weather = getWeather("Bitola")

    return render_template('weather.html',
                           city=weather['city'],
                           country=weather['country'],
                           temp=round(weather['temp'] - 276.16, 2),
                           description=weather['description'],
                           min_temp=round(weather['temp_min'] - 276.16, 2),
                           max_temp=round(weather['temp_max'] - 276.16, 2),
                           feelslike=round(weather['feels_like'] - 276.16, 2),
                           icon=weather['icon'],
                           humidity=weather['humidity'],
                           windspd=weather['wind_speed'],
                           wind_dir=weather['wind_dir']
                           )


def getWeather(city):
    r = requests.get(API_URL.format(city, API_KEY)).json()
    print(r)
    weather = {
        'city': city,
        'country': r['sys']['country'],
        'temp': r['main']['temp'],
        'feels_like': r['main']['feels_like'],
        'temp_min': r['main']['temp_min'],
        'temp_max': r['main']['temp_max'],
        'description': str(r['weather'][0]['description']).title(),
        'icon': r['weather'][0]['icon'],
        'wind_speed': r['wind']['speed'],
        'humidity': r['main']['humidity'],
        'wind_dir': degToCompass(r['wind']['deg']),

    }
    print(weather)
    return weather
