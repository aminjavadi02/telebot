import mysql.connector
from database import config

def add_group(id):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = ('INSERT INTO telgroups (group_id) VALUES (%s)')
    cursor.execute(sql,(id,))
    db.commit()

def get_groups():
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = ('SELECT * FROM telgroups')
    cursor.execute(sql)
    groups = cursor.fetchall()
    groupList = []
    for group in groups:
        groupList.append(group[1])
    return groupList

def delete_group(group_id):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute(('DELETE FROM telgroups WHERE group_id = {}'.format(group_id)))
    db.commit()