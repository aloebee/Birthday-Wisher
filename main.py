import requests
from twilio.rest import Client
import os

MY_LAT = 44.630400
MY_LONG = -79.672107
api_key = os.environ.get("OWM_API_KEY")
url= "https://api.openweathermap.org/data/2.5/weather"

parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "units": "metric",
    "cnt": 4,
}

response = requests.get(url, params=parameters)
response.raise_for_status()

data = response.json()
weather_code = data["weather"][0]["id"]
weather_desc = data["weather"][0]["description"]
# print(weather_code)
# print(weather_desc)

print(weather_code)

# if 600<= weather_code <= 622:
if weather_code >= 800:
    account_sid = os.environ.get("ACCOUNT_SID")
    auth_token = os.environ.get("AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Go skiing! {weather_desc}",
        from_='whatsapp:+14155238886',
        to='whatsapp:+16476673284'
    )
    print(message.status)
