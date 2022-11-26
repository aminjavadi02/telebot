from database import cursor,db

def create_admin(id):
    sql = ("INSERT INTO botadmin(admin_id) VALUES (%s)")
    cursor.execute(sql,(id,)) # , after id is imporatnt (id,)
    db.commit()
    admin_id = cursor.lastrowid
    print("added admin {}".format(admin_id))


create_admin('275521373')