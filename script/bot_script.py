import logging
import os
from datetime import datetime

import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from telebot import types
from telebot.apihelper import ApiTelegramException

from db import *
from station import *

# ------------- Local methods ---------------------


def clean_input(user_input):
    return [
        x.strip().lower().replace(" ", "-")
        for x in user_input.split(f" ", 1)[1].split(",")
    ]


def print_message(user_id, interested_stations):
    issues = [
        stations.get_current_update(stations.clean_name(station))
        for station in interested_stations
    ]
    current = datetime.now().strftime("%Y-%-m-%-d %H:%M:%S")
    msg = []

    msg.append(f"{current}\n\n")
    for issue in issues:
        msg.append(f"{issue}\n\n")

    bot.send_message(chat_id=user_id, text="".join(msg))


def broadcast():
    scheduled_users = db.get_all_scheduled_users()
    for user in scheduled_users:
        try:
            bot.send_message(chat_id=user,
                             text=print_message(user['_id'],
                                                user['scheduled_stations']))
        except ApiTelegramException as e:
            continue


if __name__ == "__main__":
    # Config
    load_dotenv()
    API_TOKEN = os.getenv("BOT_TOKEN")
    bot = telebot.TeleBot(API_TOKEN)

    logging.basicConfig(filename='bot.log',
                        level=logging.INFO,
                        format='%(asctime)s:%(message)s')
    stations = Stations()
    db = Mongodb()
    bot_user_collection = db.bot_user_collection
    bot_scheduled_user_collection = db.scheduled_user_collection
    commands = [
        ("get", f"Get the station(s) information (E.g. /get temple, euston)"),
        ("schedule",
         f"Schedule a daily update at 8AM (E.g. /schedule temple)"),
        ("delete", f"Remove existing update schedule"),
    ]
    print(f"The bot has started.")

# ------------ Bot commands -----------------------


@bot.message_handler(commands=["start", "help"])
def start(message):
    markup = types.InlineKeyboardMarkup()
    for command in commands:
        markup.add(
            types.InlineKeyboardButton(text=f"/{command[0]} - {command[1]}",
                                       callback_data=command[0]))
    bot.send_message(chat_id=message.chat.id,
                     text="Choose a command:",
                     reply_markup=markup)


@bot.message_handler(commands=["get"])
def get(message):
    requested_stations = clean_input(message.text)
    msg = stations.print_message(requested_stations)

    if not db.check_exisiting_user(message):
        db.register_user(message)

    logging.info("User {} gets {}".format(message.from_user.first_name,
                                          requested_stations))

    bot.reply_to(message, msg)


@bot.message_handler(commands=["schedule"])
def schedule_msg(message):
    logging.info("Received schedule message from: {}".format(
        message.from_user.first_name))
    # Get the information from the schedule input
    requested_stations = clean_input(message.text)
    # print(f"requested_stations: {requested_stations}")

    # Check if a valid station
    for station in requested_stations:
        if station.startswith(" "):
            station = station[1:]
        if station not in stations.stations_dict.keys():
            bot.reply_to(message, "Please provide valid station name(s).")
            return

    logging.info("User: {} scheduled stations: {}".format(
        message.from_user.first_name, requested_stations))

    bot.reply_to(
        message,
        text=
        f"You have successfully subscribed the updates of the following station(s): {', '.join([x.title() for x in requested_stations])}. The update schedule is set to 8AM every morning. You can delete the schedule by typing /delete."
    )

    # Check if user has registered in schedule collection
    if db.check_exisiting_scheduled_user(message):
        db.update_user_schedule(message, requested_stations)
    else:
        db.register_user_schedule(message, requested_stations)


@bot.message_handler(commands=["delete"])
def delete_schedule(message):
    if not db.check_exisiting_scheduled_user(message):
        bot.reply_to(
            message,
            text="Please set schedule using /schedule before delete a schedule"
        )
    else:
        logging.info("User {} deleted schedule.".format(
            message.from_user.first_name))
        db.delete_schedule(message)
        bot.reply_to(
            message,
            text=
            "You have successfully deleted the udpate schedule. You will not receive the updates tomorrow."
        )


# Create a background scheduler
scheduler = BackgroundScheduler()

scheduler.add_job(broadcast,
                  'interval',
                  days=1,
                  start_date='2023-01-17 08:00:00',
                  timezone='UTC')

scheduler.start()

# Start the bot
bot.polling()
