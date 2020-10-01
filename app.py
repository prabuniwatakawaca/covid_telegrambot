from telebot import TeleBot
from datetime import date, timedelta
import requests

TOKEN = "BOT TOKEN"
WELCOME = "This bot is created by [@ramadhantriyant](tg://user?id=936028661)"
HELP = "Just enter country name (_ex_: Indonesia or Thailand)"

bot = TeleBot(TOKEN, parse_mode="MARKDOWN")
result = """Covid-19 Data in {} as in {}
```
Confirmed  : {} case(s)
Death      : {} dead(s)
Recovered  : {} patient(s)
Active Case: {} patient(s)
```
"""

def get_covid_data(country):
    start_day = date.today() - timedelta(days=2)
    end_day = date.today() - timedelta(days=1)
    time_window = f"from={start_day}T00:00:00Z&to={end_day}T00:00:00Z"
    res = requests.get(f"https://api.covid19api.com/total/country/{country}?{time_window}").json()
    if isinstance(res, dict):
        return "That's not a valid country. Did you learn Geography?"
    else:
        tanggal = res[-1]['Date'][:10]
        confirmed = res[-1]['Confirmed']
        deaths = res[-1]['Deaths']
        recovered = res[-1]['Recovered']
        active = res[-1]['Active']

        return result.format(country, tanggal, confirmed, deaths, recovered, active)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, WELCOME, parse_mode="markdown")
    bot.send_message(message.from_user.id, "Which country do you need Covid-19 data? (ex: indonesia)", parse_mode="markdown")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id, HELP, parse_mode="markdown")

@bot.message_handler(func=lambda m: True)
def send_data(message):
    print(message.text)
    bot.send_message(message.from_user.id, get_covid_data(message.text), parse_mode="markdown")

bot.polling()
