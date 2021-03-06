from db_setup.mongo_setup import FORUM_MONGO_CONN


async def create_announcement_pane(classroom_uid):
    try:
        resp = FORUM_MONGO_CONN[classroom_uid + '-F']['announcements']
        resp.insert_one({"first": "first announcement"})
        resp.delete_many({})
        return True
    
    except Exception as e:
        print(e)
        return False


async def post_announcement(mongo_ann_struc, classroom_uid):
    try:
        resp = FORUM_MONGO_CONN[classroom_uid + '-F']['announcements']
        resp.insert_one(mongo_ann_struc)
        return True
    except Exception as e:
        print(e)
        return False


async def get_all_announcements(classroom_uid):
    forum_id = classroom_uid + '-F'
    msgs = []
    
    try:
        resp = FORUM_MONGO_CONN[forum_id]['announcements'].find({})
        # print([i for i in resp])

        for i in resp:
            i.pop('_id')
            msgs.append(i)

        return msgs   
        
    except Exception as e:
        print(e)
        return False


async def delete_announcement(classroom_uid, announcement_id):
    forum_id = classroom_uid + '-F'
    try:
        FORUM_MONGO_CONN[forum_id]['announcements'].delete_one(
            {
                'announcement_id': announcement_id
            }
        )
        return True
    except Exception as e:
        print(e)
        return False