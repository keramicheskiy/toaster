import time
import schedule
import telebot
import threading
import random
from telebot import types
from datetime import datetime,  timedelta
from dotenv import load_dotenv
import os


load_dotenv(".env")
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode=None)
users = {}


def check_toasts():
    now = datetime.now()
    for user, done_dates in users.items():
        for done_time in done_dates:
            if done_time <= now:
                users[user].remove(done_time)
                bot.send_message(user, "𝒹 𝑜 𝓃 𝑒 .")


@bot.message_handler(commands=['start'])
def send_start(message):
    users[message.chat.id] = []
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('heat')
    itembtn2 = types.KeyboardButton('clean')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "𝒸 𝒽 𝑜 𝑜 𝓈 𝑒    𝓌 𝒾 𝓈 𝑒 𝓁 𝓎 . . .", reply_markup=markup)


@bot.message_handler()
def text_commands(message):
    chat_id = message.chat.id
    print(users[chat_id])
    if message.text == "heat":
        print("decision was made")
        if len(users[chat_id]) == 0 or len(users[chat_id]) == 1:
            done_time = datetime.now() + timedelta(seconds=random.randint(30, 1_000_000))
            users[chat_id].append(done_time)
        elif len(users[chat_id]) == 2:
            bot.reply_to(message, "𝒸 𝓁 𝑒 𝒶 𝓃 .")
    elif message.text == "clean":
        users[chat_id] = []

    print(users)
        
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    schedule.every(10).seconds.do(check_toasts)
    t = threading.Thread(target=run_scheduler)
    t.daemon = True
    t.start()
    bot.polling(none_stop=True)


# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().day.at("12:42", "Europe/Amsterdam").do(job)
# schedule.every().minute.at(":17").do(job)


