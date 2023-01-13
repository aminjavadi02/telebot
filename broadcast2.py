from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time
from database import Messages, db
import group_handler
from pyrogram import Client,filters
from pyrogram.types import Message
from admin import get_admins
from pyrogram.errors import SeeOther,Unauthorized,BadRequest,FloodWait,Forbidden,NotAcceptable,InternalServerError,RPCError
import logging
import asyncio


api_id = 25456123
api_hash = "01a09a056dc7192a585818c04fcc088e"

client = Client("mybot",api_id, api_hash)

paused = False


@client.on_message(filters.user(get_admins()))
def start_bc(c:Client,m:Message):
    global paused
    if db.is_closed():
        db.connect()
    text = m.text
    if(text == "!start_bc"):
        if paused == True:
            scheduler.resume()
            paused = False
            m.edit('ok')
            m.delete()

@client.on_message(filters.user(get_admins()),group=5)
def stop_bc(c:Client,m:Message):
    global paused
    if db.is_closed():
        db.connect()
    text = m.text
    if(text == "!stop_bc"):
        if paused == False:
            scheduler.pause()
            paused = True
            m.edit('ok')
            m.delete()

            
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler('broadcast.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_messages(category):
    messages = Messages.select().where(Messages.category == category).namedtuples()
    message_list = []
    for message in messages:
        message_list.append(message)
    return message_list


@client.on_message(filters.user(get_admins()),group=1)
def group_add(c:Client,m:Message):
    if db.is_closed():
        db.connect()
    text = m.text
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
    if not db.is_closed():
        db.close()

@client.on_message(filters.user(get_admins()),group=2)
def del_group(c:Client,m:Message):
    if db.is_closed():
        db.connect()
    text = m.text
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
    if not db.is_closed():
        db.close()

async def broadcast(message_category,c:Client):
    if db.is_closed():
        db.connect()
    messages = Messages.select().where(Messages.category == message_category).namedtuples()
    groupList = group_handler.get_groups()
    if(len(groupList) > 0 and len(messages) > 0 ):
        for message in messages:
            await asyncio.sleep(1)
            for group_id in groupList:
                try:
                    await c.forward_messages(int(group_id), int(message.channel_id), int(message.message_id))
                    await asyncio.sleep(0.5)
                except SeeOther as seeother:
                    logger.error(seeother)
                    continue

                except Unauthorized as unauthorized:
                    logger.error(unauthorized)
                    continue

                except NotAcceptable as not_acceptable:
                    logger.error(not_acceptable)
                    continue

                except InternalServerError as internal_error:
                    logger.error(internal_error)
                    continue

                except BadRequest as badRequest:
                    if(badRequest.ID == "MESSAGE_ID_INVALID"):
                        Messages.delete().where(Messages.message_id == message.message_id).execute()
                        continue
                    elif(badRequest.ID == "PEER_ID_INVALID"):
                        group_handler.delete_group(group_id)
                        if(group_id in groupList):
                            groupList.remove(group_id)
                        continue
                except FloodWait as floodWait:
                    time.sleep(floodWait.value)
                    logger.error(floodWait)
                    continue
                except Forbidden as forbidden:
                    logger.error(forbidden)
                    continue

                except RPCError as error:
                    logger.error(error)
                    continue
                
                except TimeoutError as timeoutError:
                    logger.error(timeoutError)
                    continue

                except ConnectionError as error:
                    if(error.args[0] == "Client has not been started yet"):
                        time.sleep(60)
                        logger.error(error)
                        continue

                except Exception as err:
                    logger.error(err)
                    continue
    if not db.is_closed():
        db.close()


# scheduler = AsyncIOScheduler()
scheduler = AsyncIOScheduler(job_defaults={'max_instances': 6})
scheduler.add_job(broadcast, "interval", ["normal", client] , seconds=20)
scheduler.add_job(broadcast, "interval", ["fast", client] , seconds=10)


try:
    scheduler.start()
    client.run()
    
except ConnectionError as e:
    logger.error(e)
    pass