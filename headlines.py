from flask import Flask, render_template, request
import feedparser
import requests, json

app = Flask(__name__)

RSS_FEEDS = {
    'bbc':'http://feeds.bbci.co.uk/news/world/africa/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition_africa.rss',
    'punch': 'https://rss.punchng.com/v1/category/latest_news'
    }

DEFAULTS = {
    'publication':'bbc',
    'city': 'Ibadan'
}

API_KEYS = {
    'openexchangerates': '343d5789368b4ef0b164573b168bf50f',
    'openweathermap' :  '4a3392ac7e9d7fd9745660307c68d2e2'
}

# Using a country's currency code,
# Return a dictionary containing the rate & currency
def get_exchange_rate(currency_code):
    currency_url = 'https://openexchangerates.org/api/latest.json'
    complete_url = currency_url + '?app_id='+'343d5789368b4ef0b164573b168bf50f' + "&" + currency_code
    rate = requests.get(complete_url).json()
    rates = {
        'rate':rate['rates'][currency_code],
        'currency':currency_code
    }
    return rates

def parseCurrency(weatherInfo):
    weather_code = weatherInfo['country']
    currency_code = get_currency_code(weather_code)
    return get_exchange_rate(currency_code)
    # return a dictionary



# Obtain a country's currency code using its weather_code
def get_currency_code(weather_code):
    countries_url='http://country.io/currency.json'
    count_codes = requests.get(countries_url).json()
    for id in count_codes:
        if (id == weather_code):
            currency_code = count_codes[weather_code]
    return currency_code
    

# Obtain a city's weather information using openweatherwap's API
openWeather_key = '4a3392ac7e9d7fd9745660307c68d2e2'
def get_weather(city_name):
    url = 'http://api.openweathermap.org/data/2.5/weather?'
    complete_url = url + 'q='+city_name+'&appid='+ openWeather_key
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


@app.route('/')
def getNews():
    city_query = request.args.get("city")
    publication_query = request.args.get("publication")
    if (city_query == None):
        city_query = DEFAULTS['city']
    else:
        city_query = city_query
    # publication_query="bbc"
    # ?publication=punch
    if not publication_query or publication_query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = publication_query.lower()
    
    weather = parseWeather(city_query)
    currencyInfo = parseCurrency(weather)

    # exchangeRates = 6
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html", articles=feed['entries'], publisher=publication.upper(), weather=weather, currency=currencyInfo)
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)