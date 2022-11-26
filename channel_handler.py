import mysql.connector
from database import config,r
from database import bot


def get_redis_channels():
    if(r.exists('telchannels')):
        length = r.llen('telchannels')
        r_channels = r.lrange('telchannels',0,length)
        channels = []
        for i in r_channels:
            channels.append(bytes.decode(i))
        return channels



def get_sql_channels():
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = ('SELECT * FROM telchannels')
    cursor.execute(sql)
    channels = cursor.fetchall()
    channelList = []
    for channel in channels:
        channelList.append(channel[2])
    return channelList


def channel_is_saved(id):
    result = False
    r_channel_list = get_redis_channels()
    if id not in r_channel_list:
        sql_channel_list = get_sql_channels()
        if id not in sql_channel_list:
            result = False
        else:
            update_redis_channels(id)
            result = True
    else:
        result = True
    return result



def add_channel(name,id):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = ('INSERT INTO telchannels (channel_name,channel_id) VALUES (%s,%s)')
    cursor.execute(sql,(name,id))
    db.commit()
    r.rpush('telchannels',id)



def get_channel_id(message):
    if not message.forward_from_chat == None:
        if(message.forward_from_chat.type == 'channel'):
            channel_id = message.forward_from_chat.id
            channel_name = message.forward_from_chat.title
            if not channel_is_saved(str(channel_id)):
                add_channel(channel_name,channel_id)
                bot.reply_to(message,'done!')
                # delete msg after 5 sec
            else:
                bot.reply_to(message,'already have it!')
                # delete msg after 5 sec
        else:
            bot.reply_to(message,'this aint no channel')
    else:
        bot.reply_to(message,'this aint no channel')

def channel_is_verified(id):
    result = False
    r_channels = get_redis_channels()
    if str(id) in r_channels:
        result = True
    else:
        sql_channels = get_sql_channels()
        if str(id) in sql_channels:
            update_redis_channels(str(id))
            result = True
        else:
            result = False
    return result


def get_sql_channels():
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = ('SELECT * FROM telchannels')
    cursor.execute(sql)
    channels = cursor.fetchall()
    channelList = []
    for channel in channels:
        channelList.append(channel[2])
    return channelList


def update_redis_channels(id):
    r.rpush('telchannels',id)