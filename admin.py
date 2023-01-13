from database import Admin

def is_admin(id):
    result = False
    query = Admin.select(Admin.admin_id).where(Admin.admin_id == id).namedtuples()
    admin_list = []
    for admin in query:
        admin_list.append(admin.admin_id)
    if str(id) in admin_list:
        result = True
    return result

def get_admins():
    admin_list = []
    query = Admin.select(Admin.admin_id).namedtuples()
    for admin in query:
        admin_list.append(int(admin.admin_id))
    return admin_list