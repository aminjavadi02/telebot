from database import cursor,db
import mysql.connector
from database import config

def create_admin(id):
    sql = ("INSERT INTO botadmin(admin_id) VALUES (%s)")
    cursor.execute(sql,(id,)) # , after id is imporatnt (id,)
    db.commit()
    admin_id = cursor.lastrowid
    print("added admin {}".format(admin_id))


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


# create_admin('275521373')


