import group_handler
from database import config,bot
import message_handler
import channel_handler
import mysql.connector

@bot.message_handler(commands=['new_group'])
def new_group(message):
    if is_admin(message.from_user.id):
        if(message.chat.type == 'group' or message.chat.type == 'supergroup'):
            groupList = group_handler.get_groups()
            if str(message.chat.id) not in groupList:
                group_handler.add_group(message.chat.title,message.chat.id)
                
                msg = bot.reply_to(message,'انجام شد')
                message_handler.delete_message(msg,bot)
            else:
                msg = bot.reply_to(message,'این گروه قبلا ثبت شده است')
                message_handler.delete_message(msg,bot)
        else:
            msg = bot.reply_to(message,'اینجا گروه نیست')
            message_handler.delete_message(msg,bot)


@bot.message_handler(commands=['new_channel'])
def new_channel(message):
    if is_admin(message.from_user.id):
        msg = bot.reply_to(message,"""\
            یک پیام از کانال مورد نظر به اینجا فوروارد کن
            """)
        bot.register_next_step_handler(msg,channel_handler.get_channel_id)


# has caption
@bot.channel_post_handler(content_types=['photo','voice','video','audio'])
def get_channel_posts(message):
    if (channel_handler.channel_is_verified(message.chat.id)):
        message_handler.check_message_with_caption(message)


@bot.channel_post_handler(content_types=['text'])
def get_channel_posts(message):
    if (channel_handler.channel_is_verified(message.chat.id)):
        message_handler.check_message_with_text(message)


# is only text
@bot.edited_channel_post_handler(content_types=['text'])
def edit_message(message):
    if (channel_handler.channel_is_verified(message.chat.id)):
        message_handler.check_message_with_text(message)
       

@bot.edited_channel_post_handler(content_types=['photo','voice','video','audio'])
def get_channel_posts(message):
    if (channel_handler.channel_is_verified(message.chat.id)):
        message_handler.check_message_with_caption(message)



def is_admin(id):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = ('SELECT * FROM botadmin')
    cursor.execute(sql)
    admins = cursor.fetchall()
    adminList = [];
    for admin in admins:
        adminList.append(admin[1])
    if str(id) in adminList:
        return True
    else:
        return False



bot.infinity_polling()