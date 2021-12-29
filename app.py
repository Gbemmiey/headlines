from dotenv import load_dotenv
from flask import Flask, render_template, request, make_response
import feedparser
import requests
import os
import datetime

app = Flask(__name__)
load_dotenv()

RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/world/africa/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition_africa.rss',
    'punch': 'https://rss.punchng.com/v1/category/latest_news'
}

DEFAULTS = {
    'publication': 'bbc',
    'city': 'Ibadan'
}

API_KEYS = {
    'openexchangerates': os.getenv('openexchangerates'),
    'openweathermap': os.getenv('openweathermap')
}


# Using a country's currency code,
# Return a dictionary containing the rate & currency
def get_exchange_rate(currency_code):
    currency_url = 'https://openexchangerates.org/api/latest.json'
    complete_url = currency_url + '?app_id=' + API_KEYS['openexchangerates'] + "&" + currency_code
    rate = requests.get(complete_url).json()
    rates = {
        'rate': rate['rates'][currency_code],
        'currency': currency_code
    }
    return rates


def parseCurrency(weatherInfo):
    weather_code = weatherInfo['country']
    currency_code = get_currency_code(weather_code)
    return get_exchange_rate(currency_code)
    # return a dictionary


# Obtain a country's currency code using its weather_code
def get_currency_code(weather_code):
    countries_url = 'http://country.io/currency.json'
    count_codes = requests.get(countries_url).json()
    for id in count_codes:
        if id == weather_code:
            currency_code = count_codes[weather_code]
    return currency_code


# Obtain a city's weather information using openweatherwap's API
def get_weather(city_name):
    url = 'http://api.openweathermap.org/data/2.5/weather?'
    complete_url = url + 'q=' + city_name + '&appid=' + API_KEYS['openweathermap']
    current_weather = requests.get(complete_url).json()
    return current_weather


def parseWeather(city_name):
    raw_weather = get_weather(city_name)
    summary = raw_weather['weather']
    description = summary[0]['description']
    # C temp = Kelvin - 273
    parsedTemp = raw_weather['main']['temp']
    degrees_Celsius = int(parsedTemp) - 273
    city = raw_weather['name']
    country = raw_weather['sys']['country']
    weather = {
        'city': city,
        'country': country,
        'description': description,
        'temp': degrees_Celsius
    }
    return weather


# retrieve user's default publication and city
def getCookies():
    cookie_publication = request.cookies.get("publication")
    cookie_city = request.cookies.get("city")
    return cookie_publication, cookie_city


# set cookies about the user's preference
def setCookies(response, cookie_publication, cookie_city):
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", cookie_publication, expires=expires)
    response.set_cookie("city", cookie_city, expires=expires)


def retrieveValues():
    user_publication, user_city = getCookies()
    publication = request.args.get("publication")
    if not publication:
        publication = user_publication
        if not publication:
            publication = DEFAULTS["publication"]

    city = request.args.get("city")
    if not city:
        city = user_city
        if not city:
            city = DEFAULTS["city"]
    return publication, city


@app.route('/')
def getNews():
    publication, city = retrieveValues()
    weather = parseWeather(city)
    currencyInfo = parseCurrency(weather)
    feed = feedparser.parse(RSS_FEEDS[publication])

    template = render_template("home.html", articles=feed['entries'], publisher=publication.upper(),
                               weather=weather, currency=currencyInfo, PUBLICATIONS=RSS_FEEDS)

    response = make_response(template)
    setCookies(response, publication, city)
    return response


if __name__ == "__main__":
    app.run(debug=True)
