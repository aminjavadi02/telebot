import telebot

from database import cursor


# bot connection
bot = telebot.TeleBot("5913782753:AAEMbU1SELdfS6o-pIcwiCxwLdWA1omGwNk")

@bot.message_handler(commands=['add_group'])
def add_group(message):
    sql = ('SELECT * FROM telgroups')
    cursor.execute(sql)
    groups = cursor.fetchall()
    groupList = []
    for group in groups:
        groupList.append(group[2])
    if str(message.chat.id) not in groupList:
        print('new group')
        print(groupList)
        print(message.chat.id)
    else:
        print('already added')
        print(groupList)
            
            # print(message.chat.id)
        # else:
        #     print('match records')
    # bot.reply_to(message,groups)
        # add it



bot.infinity_polling()





















# # only do what you have to do

# r.mset({'regular_time':'5'})
# r.mset({'fast_time':2})



# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
# 	bot.reply_to(message, r.get('ali'))




# # controller:
# # new group

# @bot.message_handler(commands=['new_group'])
# def add_group(message):
#     # group_id = message.chat.id
#     # groups = r.get('groups')
#     # if there is no groups yet
#     if not groups :
#         # r.lpush('groupsList',group_id)
#     # if theres groups but dsnt inc grp_id
#     elif not group_id in groups:
#         # r.lpush('groupsList',group_id)
    
#     # print(r.get('groupsList'))

# # get incoming posts and changes
# # orginze to save in special group or delete/edit
# # deal with database
# # brodcast

# # *********************

# # model:
# # update database actions:
# # (lock process, save current index, do the update, resume the process from that index)

# # add new group
#     # save group id in "groups"
#     # update the list, running in app

# # add a new channel post

# # edit a channel post

# # delete a channel post

# # **********************************















# bot.infinity_polling()