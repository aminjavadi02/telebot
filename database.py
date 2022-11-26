import mysql.connector
import redis
import telebot

# bot connection
bot = telebot.TeleBot("5913782753:AAEMbU1SELdfS6o-pIcwiCxwLdWA1omGwNk")

# mysql
config = {
    'user':'aminbot',
    'password':'Dickhead@8585',
    'host':'localhost',
    'database':'telebot' # this line should be added after running setup.py
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

# cache
r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    password='')

# # r.mset({'ali':'mmd'}) redis db example