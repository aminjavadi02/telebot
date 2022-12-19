import group_handler
from database import config,bot
import message_handler
import channel_handler
import mysql.connector
import time
import requests
import emoji

@bot.message_handler(commands=['start'])
def start(message):
    if(is_admin(message.from_user.id)):
        welcome_msg = '''
        سلام
        به ربات خودت خوش اومدی
        لیست دستورهای ربات:

        {} اضافه کردن کانال

        {} /new_channel
        
        نکته:
        این دستور رو فقط توی همین چت با ربات بزن


        {} حذف کانال

        {} /del_channel

        نکته:
        این دستور رو فقط توی همین چت با ربات بزن


        {} اضافه کردن گروه

        {} /new_group

        نکته:
        این دستور رو داخل گروهی که ربات توش عضوه بزن


        {} حذف گروه

        {} /del_group

        نکته:
        این دستور رو داخل گروهی که ربات توش عضوه بزن


        {} نحوه کار:
        1- داخل کانال مورد نظر ربات رو عضو و ادمین کن
        2- دستور اضافه کردن کانال رو داخل چت ربات بزن (نه داخل کانال)
        3- یه پیام از کانالت به چت ربات فوروارد کن تا کانالت شناسایی بشه
        4- توی گروهی که میخوای ربات رو عضو کن
        5- دستور اضافه کردن گروه رو کف گروه بزن
        6- پیام هایی که از این به بعد توی کانال بذاری داخل این گروه فوروارد میشن :)


        {} نکته های مهم:

        1- پیام های با استیکر آتش {} سریع تر از بقیه ارسال میشن
        2- برای متوقف کردن ارسال یه پیام استیکر ضربدر{} یا گل{} بذار داخلش
        3-  اگه پیامی که میخوای متوقفش کنی قبلا داخلش استیکر آتیش داره، حتما آتیش ها رو پاک کن بعد ضربدر بذار



        '''.format(
            emoji.emojize(':diamond_with_a_dot:'),
            emoji.emojize(':robot:'),
            emoji.emojize(':diamond_with_a_dot:'),
            emoji.emojize(':robot:'),
            emoji.emojize(':diamond_with_a_dot:'),
            emoji.emojize(':robot:'),
            emoji.emojize(':diamond_with_a_dot:'),
            emoji.emojize(':robot:'),

            emoji.emojize(':electric_plug:'),
            emoji.emojize(':firecracker:'),

            emoji.emojize(':fire:'),
            emoji.emojize(':cross_mark:'),
            emoji.emojize(':rose:'),
        )
        bot.reply_to(message,welcome_msg)


@bot.message_handler(commands=['test_cm'])
def test_cm(message):
    # bot.reply_to(message,message)
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = ('SELECT * FROM botadmin')
    cursor.execute(sql)
    admins = cursor.fetchall()
    adminList = [];
    for admin in admins:
        adminList.append(admin[1])
    for i in adminList:
        print(type(i))

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


@bot.message_handler(commands=['del_group'])
def del_group(message):
    if is_admin(message.from_user.id):
        if(message.chat.type == 'group' or message.chat.type == 'supergroup'):
            groupList = group_handler.get_groups()
            if str(message.chat.id) in groupList:
                group_handler.delete_group(message.chat.id)
                
                msg = bot.reply_to(message,'انجام شد')
                message_handler.delete_message(msg,bot)
            else:
                msg = bot.reply_to(message,'این گروه در دیتابیس وجود ندارد')
                message_handler.delete_message(msg,bot)
        else:
            msg = bot.reply_to(message,'اینجا گروه نیست')
            message_handler.delete_message(msg,bot)


# check if inside the bot
@bot.message_handler(commands=['new_channel'])
def new_channel(message):
    if is_admin(message.from_user.id):
        msg = bot.reply_to(message,"""\
            یک پیام از کانال مورد نظر به اینجا فوروارد کن
            """)
        bot.register_next_step_handler(msg,channel_handler.get_channel_id)


@bot.message_handler(commands=['del_channel'])
def def_channle(message):
    if is_admin(message.from_user.id):
        msg = bot.reply_to(message,"""\
            یک پیام از کانال مورد نظر به اینجا فوروارد کن
            """)
        bot.register_next_step_handler(msg,channel_handler.del_channle_handler)
    


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


try:
    bot.infinity_polling()
except Exception as e:
    if(isinstance(e,requests.exceptions.ConnectionError)):
        time.sleep(60)
        pass
    else:
        print(e)