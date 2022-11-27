import emoji
import mysql.connector
from database import config
import time

def check_message_with_caption(message):
    if not message.caption == None:
        emojiList = emoji.distinct_emoji_list(message.caption)
        if emoji.emojize(":fire:") in emojiList:
            set_message(message,'fast')
        elif emoji.emojize("✖️") in emojiList:
            finished_message(message)
        elif emoji.emojize(":rose:") in emojiList:
            finished_message(message)
        else:
            set_message(message,'normal')
    else:
        print(message)
        set_message(message,'normal')

def check_message_with_text(message):
    # check if message is not a command
    if not message.text == None:
        emojiList = emoji.distinct_emoji_list(message.text)
        if emoji.emojize(":fire:") in emojiList:
            set_message(message,'fast')
        elif emoji.emojize("✖️") in emojiList:
            finished_message(message)
        elif emoji.emojize(":rose:") in emojiList:
            finished_message(message)
        else:
            set_message(message,'normal')
    else:
        print(message)
        set_message(message,'normal')


def set_message(message,mode):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = ('INSERT INTO messages (channel_id,message_id,category) VALUES (%s,%s,%s)')
    cursor.execute(sql,(message.chat.id,message.message_id,mode))
    db.commit()

def finished_message(message):
    if(message_exists(message)):
        print('you')
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        sql = ('DELETE FROM messages WHERE channel_id= %s AND message_id = %s')
        cursor.execute(sql,(message.chat.id,message.message_id,))
        db.commit()

def message_exists(message):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = ('SELECT * FROM messages WHERE channel_id = %s')
    cursor.execute(sql,(message.chat.id,)) # , after chat.id is important (message.chat.id,)
    sql_messages = cursor.fetchall()
    result = False
    message_list = []
    for i in sql_messages:
        message_list.append(i[2])
    if str(message.message_id) in message_list:
        result = True
    return result

# make connection to dbs and put them inside the list

def delete_message(reply,command,bot):
    time.sleep(5)
    bot.delete_message(reply.chat.id,reply.message_id)
    bot.delete_message(command.chat.id,command.message_id)


def get_all_messages_list():
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = ('SELECT * FROM messages')
    cursor.execute(sql)
    sql_messages = cursor.fetchall()
    return sql_messages