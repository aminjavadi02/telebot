from database import bot
import schedule
import time
import mysql.connector
from database import config
import channel_handler
import message_handler
import group_handler
import logging,logging.handlers
import requests

logger = logging.getLogger()
logger.addHandler(logging.handlers.SMTPHandler(
    mailhost=("smtp.mailtrap.io", 2525),
    fromaddr="error@telgrambot.com",
    toaddrs="solver@telegrambot",
    subject="EXCEPTION",
    credentials=("032a3b288a5aa2", "c100cefcba3755"),
    secure=()))

def get_messages(sql):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute(sql)
    messages = cursor.fetchall()
    return messages

def broadcast(message_mode):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    groupList = group_handler.get_groups()
    messages = get_messages(message_mode)
    if(len(groupList) > 0 and len(messages) > 0 ):
        try:
            for message in messages:
                for i in groupList:
                    bot.forward_message(int(i),int(message[1]),int(message[2]))
        except Exception as e:
            if(isinstance(e,requests.exceptions.ConnectionError)):
                time.sleep(60)
                pass
            elif(hasattr(e,'description')):
                if(
                    (e.description == 'Bad Request: message to forward not found')
                    or
                    (e.description == 'Bad Request: MESSAGE_ID_INVALID')
                ):
                    print(e)
                    sql3 = ('DELETE FROM messages WHERE id = {}'.format(message[0]))
                    cursor.execute(sql3)
                    db.commit()
                    if(message in messages):
                        messages.remove(message)
                    pass
                elif(
                        (e.description == 'Forbidden: bot was kicked from the supergroup chat')
                        or
                        (e.description == 'Forbidden: bot was kicked from the group chat')
                    ):
                    group_handler.delete_group(i)
                    if(i in groupList):
                        groupList.remove(i)
                    pass
                elif(e.description == 'Forbidden: bot was kicked from the channel chat'):
                    print(e)
                    channel_handler.delete_channel(message[1])
                    message_handler.delete_channel_messages(message[1])
                    pass
                elif(e.description == 'Bad Request: group chat was upgraded to a supergroup chat'):
                    print(e)
                    group_handler.delete_group(i)
                    if(i in groupList):
                        groupList.remove(i)
                    pass
                elif(e.description == 'Forbidden: bot is not a member of the channel chat'):
                    channel_handler.delete_channel(message[1])
                    message_handler.delete_channel_messages(message[1])
                    pass
                elif(e.description == "Bad Request: PEER_ID_INVALID"):
                    group_handler.delete_group(i)
                    if(i in groupList):
                        groupList.remove(i)
                    pass
                else:
                    print(e)
                    pass
            elif(hasattr(e,'error_code')):
                if(e.error_code == 429):
                    print(e)
                    time.sleep(300)
                else:
                    print(e)
                    print(message)
                    print(i)
                    logging.exception(e)
                    pass
            else:
                print(e)
                pass
            pass

sql_normal = ("SELECT * FROM messages WHERE category = 'normal'")
sql_fast = sql = ("SELECT * FROM messages WHERE category = 'fast'")

# schedule.every(3).minutes.do(broadcast,sql_fast)
# schedule.every(7).minutes.do(broadcast,sql_normal)

schedule.every(5).seconds.do(broadcast,sql_fast)
schedule.every(10).seconds.do(broadcast,sql_normal)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except Exception as e:
    print(e)
    pass
