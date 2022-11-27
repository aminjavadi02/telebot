import group_handler
from database import config,bot
import message_handler
import channel_handler
import mysql.connector

@bot.message_handler(commands=['new_group'])
def new_group(message):
    if is_admin(message.from_user.id):
        if(message.chat.type == 'supergroup'):
            groupList = group_handler.get_groups()
            if str(message.chat.id) not in groupList:
                group_handler.add_group(message.chat.title,message.chat.id)
                bot.reply_to(message,'done!')
                # delete msg after 5 sec
            else:
                bot.reply_to(message,'already have it!')
                # delete msg after 5 sec
        else:
            bot.reply_to(message,'this aint no group')


@bot.message_handler(commands=['new_channel'])
def new_channel(message):
    if is_admin(message.from_user.id):
        msg = bot.reply_to(message,"""\
            hi. forward a message from the channel that you want to add
            """)
        bot.register_next_step_handler(msg,channel_handler.get_channel_id)


# has caption
@bot.channel_post_handler(content_types=['photo','voice','video','audio'])
def get_channel_posts(message):
    if (channel_handler.channel_is_verified(message.chat.id)):
        message_handler.check_message_with_caption(message)
        # الباقی رو خود چک مسج باید بده به ردیس و بعدش تابع برادکست همواره پیام ها رو از ردیس بگیره و بفرسته کاری به این نداشته باشه دیگه
@bot.channel_post_handler(content_types=['text'])
def get_channel_posts(message):
    if (channel_handler.channel_is_verified(message.chat.id)):
        message_handler.check_message_with_text(message)

    # check message
    # put in correct list in redis,sql
    # read from redis every time and brodcast it
    # brodcast

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


# bot.forward_message(-1001897148828,message.chat.id,message.message_id)