import requests, json, os

from glom import glom

def fetch_weather():
    weather = requests.get(f'http://api.weatherapi.com/v1/marine.json?key={os.environ.get("WEATHERAPI_KEY")}&q=Skidegate&days=1').json()

    spec = {
        'date': ('forecast.forecastday.0.date'),
        'maxtemp': ('forecast.forecastday.0.day.maxtemp_c'),
        'maxwind': ('forecast.forecastday.0.day.maxwind_kph'),
        'mintemp': ('forecast.forecastday.0.day.mintemp_c'),
        'precip': ('forecast.forecastday.0.day.totalprecip_mm'),
        'humidity': ('forecast.forecastday.0.day.avghumidity'),
        'summary': ('forecast.forecastday.0.day.condition.text'),
        'tides': ('forecast.forecastday.0.day.tides.0.tide'),
        'astro': ('forecast.forecastday.0.astro'),
    }

    return glom(weather, spec)
