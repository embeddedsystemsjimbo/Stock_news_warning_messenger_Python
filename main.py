import requests
from datetime import date
from twilio.rest import Client
import pandas

alpha_vantage_api_key = "insert API code here"
newsapi_key = "insert API code here"
twilio_api_key = "insert API code here"

data = pandas.read_csv("./stock_list.csv")

stock_list = [{"Symbol": row.Symbol, "Company": row.Company_Name} for index, row in data.iterrows()]


def get_stock_percentage_change(ticker_symbol):

    alpha_vantage_url = "https://www.alphavantage.co/query"

    alpha_vantage_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker_symbol,
        "apikey": alpha_vantage_api_key,
    }

    response = requests.get(url=alpha_vantage_url, params=alpha_vantage_params)
    response.raise_for_status()
    stock_price_data = response.json()

    monthly_price_list = [float(info["4. close"]) for index, info in stock_price_data["Time Series (Daily)"].items()]

    yesterday, before_yesterday = monthly_price_list[1:3]    # yesterday, day before yesterday

    difference = yesterday - before_yesterday

    percent = (difference / yesterday) * 100

    return round(percent, 1)


def get_news(company_name):

    newsapi_url = "https://newsapi.org/v2/everything"

    newsapi_params = {
        "qInTitle": company_name,
        "from": date.today(),
        "language": "en",
        "sortBy": "popularity",
        "apiKey": newsapi_key,
    }

    response = requests.get(url=newsapi_url, params=newsapi_params)
    response.raise_for_status()
    news_data = response.json()

    return news_data["articles"][:3]


def create_percentage_tag(price):

    if price > 0:
        return f"🔺{price}%"
    elif price == 0:
        return "0.0"
    else:
        return f"🔻{abs(price)}%"


def sent_sms(symbol, percent, description, message, url):

    account_sid = 'ACec297af4b447a1530b6e5160caa04214'

    client = Client(account_sid, twilio_api_key)

    message = client.messages.create(
        messaging_service_sid='insert your twillio messaging id',
        body=f"({symbol}){create_percentage_tag(percent)}\n "
             f"Title: {description}\n"
             f"Brief: {message}\n"
             f"{url}",
        to='insert your phone number'
    )

    print(message.status)


for stock in stock_list:

    percentage = get_stock_percentage_change(stock["Symbol"])

    if percentage > 5 or percentage < -5:

        news_article_list = get_news(stock["Company"])

        for article in news_article_list:

            sent_sms(stock["Symbol"], percentage, article["title"], article["description"], article["url"])

