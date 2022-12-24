import mysql.connector
import telebot

# bot connection

bot = telebot.TeleBot("5861111194:AAH3nf8lnAzrVtTsNmD--Y7aT7L27DVV2Cs")

# mysql
config = {
    'user':'aminbot',
    'password':'Dickhead@8585',
    'host':'localhost',
    'database':'telebot' # this line should be added after running setup.py
}

db = mysql.connector.connect(**config)
cursor = db.cursor()