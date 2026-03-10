import requests
import datetime as dt
from twilio.rest import Client
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get stock price data using API
price_api_key = os.environ.get("PRICE_API_KEY")
price_url = "https://www.alphavantage.co/query"
price_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": price_api_key,
}

price_response = requests.get(url=price_url, params=price_parameters)
price_response.raise_for_status()
price_data = price_response.json()


# Find current date and current day's closing price
current_date = price_data["Meta Data"]["3. Last Refreshed"]
print(current_date)
current_close = float(price_data["Time Series (Daily)"][current_date]["4. close"])

current_date_list = current_date.split("-")
current_date_dt = dt.date(int(current_date_list[0]), int(current_date_list[1]), int(current_date_list[2]))

# Find prior date in string, and find prior day's closing price
prior_date_dt = current_date_dt - dt.timedelta(days=1)
prior_date = str(prior_date_dt)
print(prior_date)
last_close = float(price_data["Time Series (Daily)"][prior_date]["4. close"])

# Use the closing prices of prior day and current day, calculate price and % change
price_change = current_close - last_close
percent_change = f"{abs(round(price_change / last_close * 100,2))}%"

print(percent_change)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
news_api_key = os.environ.get("NEWS_API_KEY")

news_url = "https://newsapi.org/v2/everything"
news_parameters = {
    "apiKey": news_api_key,
    "q": COMPANY_NAME,
    "from": prior_date,
    "to": current_date,
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 3,
}
news_response = requests.get(news_url, params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()["articles"]
headline0 = news_data[0]["title"]
brief0 = news_data[0]["description"]
link0 = news_data[0]["url"]

headline1 = news_data[1]["title"]
brief1 = news_data[1]["description"]
link1 = news_data[1]["url"]

headline2 = news_data[2]["title"]
brief2 = news_data[2]["description"]
link2 = news_data[2]["url"]


# Format message
sign = ""
if price_change > 0:
    sign = "🔺"
elif price_change < 0:
    sign = "🔻"
message = (
    f"{STOCK}: {sign} {percent_change} \n"
    f"Headline: {headline0} \nBrief: {brief0} \n\n"
    f"Headline: {headline1} \nBrief: {brief1} \n\n"
    f"Headline: {headline2} \nBrief: {brief2} \nBrief: {brief2}"
)

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
client = Client(account_sid, auth_token)

message = client.messages.create(
    body=message,
    from_='whatsapp:+14155238886',
    to='whatsapp:+16476673284'
)
print(message.status)
