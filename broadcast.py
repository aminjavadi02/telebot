import message_handler
import group_handler
from database import bot
import time
def brodcast():
    while(True):
        message_list = message_handler.get_all_messages_list()
        group_list = group_handler.get_groups()
        for message in message_list:
            if message[3] == 'fast':
                time.sleep(5)
                for group in group_list:
                    bot.forward_message(int(group),int(message[1]),int(message[2]))
            elif message[3] == 'normal':
                time.sleep(60)
                for group in group_list:
                    bot.forward_message(int(group),int(message[1]),int(message[2]))




brodcast()