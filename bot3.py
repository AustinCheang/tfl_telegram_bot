from apscheduler.schedulers.background import BackgroundScheduler
import telebot

# Replace YOUR_BOT_TOKEN with your bot's API token
bot = telebot.TeleBot("token")

# Create an empty list to store subscribed users
subscribed_users = []


# Function to handle the /hello command
@bot.message_handler(commands=['hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello, welcome to my Telegram bot!")


# Function to handle the /subscribe command
@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    user_id = message.from_user.id
    if user_id not in subscribed_users:
        subscribed_users.append(user_id)
        bot.reply_to(message, "You have been subscribed")
    else:
        bot.reply_to(message, "You are already subscribed")


# Function to send the "Good Morning" message to subscribed users
def send_morning_greeting():
    for user_id in subscribed_users:
        bot.send_message(user_id, "Good Morning, {}".format(user_id))


# Create a background scheduler
scheduler = BackgroundScheduler()

# Schedule the send_morning_greeting function to run every day at 22:17
scheduler.add_job(send_morning_greeting,
                  'interval',0
                  days=1,
                  start_date='2022-08-20 23:13:00',
                  timezone='UTC')

# Start the scheduler
scheduler.start()

# Start the bot
bot.polling()