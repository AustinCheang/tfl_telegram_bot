import threading
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
from station import *
import telebot
import json

from station import *
from db import *
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler

import telegram
from telegram.ext import Updater, CommandHandler,
import logging

load_dotenv()
bot = telegram.Bot(token=os.getenv("BOT_TOKEN"))
updater = Updater(bot, update_queue=True)
dispatcher = telegram
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# writting functionality of the command
def start(update, context):
    message = 'Welcome to the bot'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
# give a name to the command and add it to the dispaatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling() 