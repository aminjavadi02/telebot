import mysql.connector
from database import config

def add_group(name,id):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = ('INSERT INTO telgroups (group_name,group_id) VALUES (%s,%s)')
    cursor.execute(sql,(name,id))
    db.commit()

def get_groups():
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = ('SELECT * FROM telgroups')
    cursor.execute(sql)
    groups = cursor.fetchall()
    groupList = []
    for group in groups:
        groupList.append(group[2])
    return groupList