import mysql.connector
from database import cursor
from mysql.connector import errorcode

DB_NAME = 'telebot'

def create_database():
    cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    print('database {} created'.format(DB_NAME))

TABLES = {}

TABLES['admin'] = (
    "CREATE TABLE `botadmin`("
    "`id` int(2) AUTO_INCREMENT UNIQUE,"
    "`admin_id` varchar(15) NOT NULL UNIQUE,"
    "PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)

TABLES['telgroup'] = (
    "CREATE TABLE `telgroups`("
    "`id` int(11) AUTO_INCREMENT UNIQUE,"
    "`group_name` varchar(50) NULL,"
    "`group_id` varchar(50) NOT NULL UNIQUE,"
    "PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)
TABLES['telchannels'] = (
    "CREATE TABLE `telchannels`("
    "`id` int(11) AUTO_INCREMENT UNIQUE,"
    "`channel_name` varchar(50) NULL,"
    "`channel_id` varchar(50) NOT NULL UNIQUE,"
    "PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)
TABLES['messages'] = (
    "CREATE TABLE `messages`("
    "`id` int(11) AUTO_INCREMENT UNIQUE PRIMARY KEY,"
    "`channel_id` varchar(50) NOT NULL,"
    "`message_id` varchar(50) NOT NULl,"
    "`category` varchar(50) NOT NULL"
    ") ENGINE=InnoDB"
)


def create_tables():
    cursor.execute("USE {}".format(DB_NAME))
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            cursor.execute(table_description)
            print('created {}'.format(table_name))
        except mysql.connector.Error as err:
            print(err.msg)



create_database()
create_tables()