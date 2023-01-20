# aus_tfl_telegram_bot

This project is a Telegram bot (`@aus_tfl_bot`) that provides users with real-time updates on disruptions and issues affecting London's Tube stations. With this bot, users can stay informed of potential delays and closures, such as those caused by staff shortages, before they travel. Additionally, users can schedule daily updates to be sent at 8AM, helping them to plan ahead and minimise any potential impact on their commutes.

Source: [Transport For London](https://tfl.gov.uk/).

## Getting Started

Step 1: Download Telegram and register an account. Go to search box and search `aus_tfl_bot` which has a green icon.

Step 2: Click `START` to start interacting with the bot.

![](./images/Screenshot%202023-01-19%20at%2003.02.00.png)

Step 3: The bot first displays all the existing commands:

1.  `/get` - Get the station(s) information
2.  `/schedule` - Schedule a daily update at 8AM
3.  `/delete` - Remove existing update schedule

Users can always check all the commands by typing `/start` and `/help`.

![Screenshot 2023-01-19 at 03.07.16](./images/Screenshot%202023-01-19%20at%2003.07.16.png)

## Example

1.  The `/get` command allows users to retrieve current reported issues for specific London Tube stations of their choice. Users can input one or multiple stations at a time, for example by typing "/get Temple, Euston" and the station names are not case-sensitive.

![Screenshot 2023-01-19 at 03.08.56](./images/Screenshot%202023-01-19%20at%2003.08.56.png)

2.  The `/schedule` command enables users to set up daily reminders for specific London Tube stations they want to monitor. The reminder is sent every morning at 8AM. Users can set reminders for multiple stations by typing "/schedule Temple, Euston" in the chat.

![Screenshot 2023-01-20 at 11.50.08](./images/Screenshot%202023-01-20%20at%2011.50.08.png)

3.  The `/delete` command enables the users to cancel any previously established schedule, thus stopping them from receiving further updates for the respective tube stations.

![Screenshot 2023-01-19 at 14.17.17](./images/Screenshot%202023-01-19%20at%2014.17.17.png)

## Future updates

The functionalities of the bot are very limited currently. There are few areas I would want to expand in the future.

1.  Providing more detailed information on the status of Tube lines and corresponding service closed time during night closure.
2.  Introducing a new command that enables users to check the arrival times of the next 5 tubes at a specific station, to aid in trip planning.
