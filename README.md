# Gym Tracker WhatsApp Bot

This project enables you to record and retrieve gym exercises through WhatsApp, using Python and Selenium. The system is designed to work with WhatsApp Web running on your computer, allowing you to interact with the bot through your phone for tracking your gym lifts, weights, and reps. Exercise data is stored in a local PostgreSQL (PSQL) database, and the app has access to an API to suggest new exercises.

## Features

- **Track Exercises**: Easily log your completed exercises, including the weight and number of reps, directly from WhatsApp.
- **Retrieve Past Data**: Access your previously logged exercises, organized by type, weight, and reps, through a simple WhatsApp message.
- **Exercise Suggestions**: The app connects to an external API that can suggest new exercises for you to try.
- **Local Storage**: All exercise data is stored in a local PostgreSQL database, allowing easy access and retrieval of your workout history.

## How It Works

1. **Setup WhatsApp Web**: The bot operates via WhatsApp Web, which needs to be open on your PC. The user creates a pinned chat called **Gym**, where they are the only member.
   
2. **Communication with WhatsApp**: Selenium is used to control the browser and automate sending and receiving messages via WhatsApp Web. The user interacts with the bot through their phone by messaging the Gym chat.

3. **Logging and Retrieving Data**: Once a message is sent about an exercise and its lift, the bot records the exercise into the PostgreSQL database. You can also send commands to retrieve previous workout data, via going through the options

4. **Exercise API**: The bot can recommend new exercises by fetching data from an external API, keeping your workouts varied and interesting.

### Requirements

- **Python 3.x**
- **PostgreSQL**: For storing your exercise data.
- **Selenium**: Used to automate WhatsApp Web interactions.
- **Google Chrome**: Latest version not supported. Version 104.0 required for Selenium.
- **ChromeDriver**: To control the Chrome browser via Selenium.

## .env file
Ensure you have the following parameters set up in your .env file
- **DB_NAME**
- **DB_USER**
- **DB_PASSWORD**
- **DB_HOST**
- **DB_PORT**

### Limitations
- **Browser Compatibility:** The project currently does not support the latest version of Google Chrome. Ensure you're using a version of Chrome that is compatible with the installed ChromeDriver.

- **WhatsApp Web:** You must have WhatsApp Web open and running on your PC at all times for the bot to function correctly.

For a Django-based alternative, check out [this project](https://github.com/Dani-r-36/django_gym).

**Note** This project was designed for my own use and hasn't been updated for others to use, but are welcome to use :)
