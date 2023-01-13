from database import Tel_group

def add_group(id):
    Tel_group.create(
        group_id = id
    )

def get_groups():
    query = Tel_group.select().namedtuples()
    groupList = []
    for group in query:
        groupList.append(group.group_id)
    return groupList

def delete_group(group_id):
    Tel_group.delete().where(Tel_group.group_id == group_id).execute()