from database import config
import emoji
from redis.commands.json.path import Path

def check_message(message):
    emojiList = emoji.distinct_emoji_list(message.text)
    if emoji.emojize(":fire:") in emojiList:
        set_message(message,'fast')
    elif emoji.emojize("✖️") in emojiList:
        finished_message(message)
    elif emoji.emojize(":rose:") in emojiList:
        finished_message(message)
    else:
        normal_message(message)

def set_message(message,mode):
    print(message,mode)

def finished_message(message):
    print('finished')

def normal_message(message):
    print('normal')



# make connection to dbs and put them inside the list