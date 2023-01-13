from database import Tel_channel
from bot import bot
import message_handler


def add_channel(id):
    Tel_channel.create(
        channel_id = id
    )

def get_channel_id(message):
    if not message.forward_from_chat == None:
        if(message.forward_from_chat.type == 'channel'):
            channel_id = message.forward_from_chat.id
            if not channel_is_verified(str(channel_id)):
                add_channel(channel_id)
                bot.reply_to(message,'انجام شد')
            else:
                bot.reply_to(message,'این کانال قبلا ثبت شده است')
        else:
            bot.reply_to(message,'این کانال نیست')
    else:
        bot.reply_to(message,'این کانال نیست')

def channel_is_verified(id):
    result = False
    channels = get_channels()
    if str(id) in channels:
        result = True
    else:
        result = False
    return result

def get_channels():
    query = Tel_channel.select(Tel_channel.channel_id).namedtuples()
    channels = []
    for channel in query:
        channels.append(channel.channel_id)
    return channels

def delete_channel(channel_id):
    Tel_channel.delete().where(Tel_channel.channel_id == channel_id).execute()
    message_handler.delete_channel_messages(channel_id)


def del_channle_handler(message):
    if not message.forward_from_chat == None:
        if(message.forward_from_chat.type == 'channel'):
            channel_id = message.forward_from_chat.id
            if channel_is_verified(str(channel_id)):
                delete_channel(channel_id)
                bot.reply_to(message,'انجام شد')
            else:
                bot.reply_to(message,'این کانال در دیتابیس وجود ندارد')
        else:
            bot.reply_to(message,'این پیام از کانال نیست')
    else:
        bot.reply_to(message,'این پیام از کانال نیست')