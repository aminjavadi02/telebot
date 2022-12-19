import mysql.connector
from database import config
from database import bot


def add_channel(id):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = ('INSERT INTO telchannels (channel_id) VALUES (%s)')
    cursor.execute(sql,(id,))
    db.commit()

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
    channelList = []
    for channel in channels:
        channelList.append(channel[1])
    if str(id) in channelList:
        result = True
    else:
        result = False
    return result

def get_channels():
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = ('SELECT * FROM telchannels')
    cursor.execute(sql)
    channels = cursor.fetchall()
    return channels

def delete_channel(channel_id):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute(('DELETE FROM telchannels WHERE channel_id = {}'.format(channel_id)))
    db.commit()


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