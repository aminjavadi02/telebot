from database import config,r
import emoji

def check_message(message):
    emojiList = emoji.distinct_emoji_list(message.text)
    if emoji.emojize(":fire:") in emojiList:
        fast_message(message)
    elif emoji.emojize("✖️") in emojiList:
        finished_message(message)
    elif emoji.emojize(":rose:") in emojiList:
        finished_message(message)
    else:
        normal_message(message)

def fast_message(message):
    print('fast')

def finished_message(message):
    print('finished')

def normal_message(message):
    print('normal')



# make connection to dbs and put them inside the list