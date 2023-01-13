from peewee import * 

DB_NAME = 'telebot'


db = MySQLDatabase(DB_NAME, host="localhost", port=3306, user="aminbot", passwd="Dickhead@8585")

class BaseModel(Model):
    class Meta:
        database = db

class Admin(BaseModel):
    admin_id = CharField(unique=True, null = False)

class Tel_group(BaseModel):
    group_id = CharField(unique=True, null = False)

class Tel_channel(BaseModel):
    channel_id = CharField(unique=True, null = False)

class Messages(BaseModel):
    channel_id = CharField(unique= False, null = False)
    message_id = CharField(unique= False, null = False)
    category = CharField(unique= False, null = False)

db.connect()
db.create_tables([Admin, Tel_channel, Tel_group, Messages])