import emoji
from database import Messages

def check_message_with_caption(message):
    if not message.caption == None:
        emojiList = emoji.distinct_emoji_list(message.caption)
        if emoji.emojize(":fire:") in emojiList:
            create_message(message,'fast')
        elif emoji.emojize(":cross_mark:") in emojiList:
            delete_finished_message(message)
        elif emoji.emojize(":rose:") in emojiList:
            delete_finished_message(message)
        else:
            create_message(message,'normal')
    else:
        create_message(message,'normal')

def check_message_with_text(message):
    # check if message is not a command
    if not message.text == None:
        emojiList = emoji.distinct_emoji_list(message.text)
        if emoji.emojize(":fire:") in emojiList:
            create_message(message,'fast')
        elif emoji.emojize(":cross_mark:") in emojiList:
            delete_finished_message(message)
        elif emoji.emojize(":rose:") in emojiList:
            delete_finished_message(message)
        else:
            create_message(message, 'normal')
    else:
        create_message(message, 'normal')

def create_message(message, category):
    Messages.create(
        channel_id = message.chat.id,
        message_id = message.message_id,
        category = category,
    )
    

def delete_finished_message(message):
    if(message_exists(message)):
        Messages.delete().where(Messages.channel_id == message.chat.id and Messages.message_id == message.message_id).execute()

def message_exists(message):
    result = False
    sql_messages = Messages.select(Messages.message_id).where(Messages.channel_id == message.chat.id and Messages.message_id == message.message_id).namedtuples()
    if(len(sql_messages) > 0):
        result = True
    return result

def delete_channel_messages(channel_id):
    Messages.delete().where(Messages.channel_id == channel_id).execute()