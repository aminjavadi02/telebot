from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time
import mysql.connector
from database import config
import group_handler
from pyrogram import Client
from pyrogram.types import Message
from admin import is_admin
from pyrogram.errors import SeeOther,Unauthorized,BadRequest,FloodWait,Forbidden,NotAcceptable,InternalServerError,RPCError
import logging



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler('broadcast.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_messages(sql):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute(sql)
    messages = cursor.fetchall()
    return messages

api_id = 25456123
api_hash = "01a09a056dc7192a585818c04fcc088e"

client = Client("mybot",api_id, api_hash)


@client.on_message(group=1)
def group_add(c:Client,m:Message):
    text = m.text
    if(hasattr(m,'from_user') and hasattr(m.from_user,'id')):
        if is_admin(m.from_user.id):
            if(text == "!new_group"):
                if(m.chat.type.value == 'group' or m.chat.type.value == 'supergroup'):
                    groupList = group_handler.get_groups()
                    if str(m.chat.id) not in groupList:
                        group_handler.add_group(m.chat.id)
                        m.edit('انجام شد')
                        m.delete()
                    else:
                        m.edit('این گروه قبلا ثبت شده است')
                        m.delete()
                else:
                    m.edit('اینجا گروه نیست')
                    m.delete()

@client.on_message(group=0)
def del_group(c:Client,m:Message):
    text = m.text
    if(hasattr(m,'from_user') and hasattr(m.from_user,'id')):
        if is_admin(m.from_user.id):
            if(text == "!del_group"):
                if(m.chat.type.value == 'group' or m.chat.type.value == 'supergroup'):
                    groupList = group_handler.get_groups()
                    if str(m.chat.id) in groupList:
                        group_handler.delete_group(m.chat.id)
                        m.edit('انجام شد')
                        m.delete()
                    else:
                        m.edit('این گروه در دیتابیس وجود ندارد')
                        m.delete()
                else:
                    m.edit('اینجا گروه نیست')
                    m.delete()

async def broadcast(message_mode,c:Client):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    groupList = group_handler.get_groups()
    messages = get_messages(message_mode)
    if(len(groupList) > 0 and len(messages) > 0 ):
        try:
            await c.start()
            for message in messages:
                for i in groupList:
                    await c.forward_messages(int(i),int(message[1]),int(message[2]))
            await c.stop()
        except SeeOther as seeother:
            logger.error(seeother)
            pass

        except Unauthorized as unauthorized:
            logger.error(unauthorized)
            pass

        except NotAcceptable as not_acceptable:
            logger.error(not_acceptable)
            pass

        except InternalServerError as internal_error:
            logger.error(internal_error)
            pass

        except BadRequest as badRequest:
            if(badRequest.ID == "MESSAGE_ID_INVALID"):
                sql = ('DELETE FROM messages WHERE id = {}'.format(message[0]))
                cursor.execute(sql)
                db.commit()
                if(message in messages):
                    messages.remove(message)
                pass
            elif(badRequest.ID == "PEER_ID_INVALID"):
                group_handler.delete_group(i)
                if(i in groupList):
                    groupList.remove(i)
                pass
        except FloodWait as floodWait:
            time.sleep(floodWait.value)
            logger.error(floodWait)
            pass

        except Forbidden as forbidden:
            logger.error(forbidden)
            pass

        except RPCError as error:
            logger.error(error)
            pass
        
        except TimeoutError as timeoutError:
            logger.error(timeoutError)
            pass

        except ConnectionError as error:
            if(error.args[0] == "Client has not been started yet"):
                time.sleep(60)
                logger.error(error)
                pass

        except Exception as err:
            logger.error(err)
            pass

sql_normal = ("SELECT * FROM messages WHERE category = 'normal'")
sql_fast = sql = ("SELECT * FROM messages WHERE category = 'fast'")


scheduler = AsyncIOScheduler()
scheduler.add_job(broadcast, "interval", [sql_normal,client] , seconds=10)
scheduler.add_job(broadcast, "interval", [sql_fast,client] , seconds=5)



try:
    scheduler.start()
    client.run()
    
except ConnectionError as e:
    logger.error(e)
    pass