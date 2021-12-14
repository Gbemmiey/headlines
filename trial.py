import requests, json
# url = 'http://api.openweathermap.org/data/2.5/weather?'
# api_key = '4a3392ac7e9d7fd9745660307c68d2e2'
# city_name = 'Lagos'

# complete_url = url + 'q='+city_name+'&appid='+api_key
# current_weather = requests.get(complete_url).json()
# print(current_weather)


openexchangerates_key = '343d5789368b4ef0b164573b168bf50f'
def get_exchange_rate(currency_code):
    currency_url = 'https://openexchangerates.org/api/latest.json?app_id='
    complete_url = currency_url + openexchangerates_key + "&symbols=" + currency_code
    rate = requests.get(complete_url).json()
    print(rate)

get_exchange_rate("NGN")

def get_currency_code(weather_code):
    countries_url='http://country.io/currency.json'
    count_codes = requests.get(countries_url).json()
    print(count_codes)
    for id in count_codes:
        if (id == "NG"):
            currency_code = count_codes[weather_code]
            print(currency_code)

# get_currency_code("NG")