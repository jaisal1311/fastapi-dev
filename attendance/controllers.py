from classrooms import models as classroom_models
from attendance import mongo as attendance_mongo
from attendance import redis as attendance_redis


async def check_user_if_creator(classroom_id, user_id):
    classroom_obj = await classroom_models.get_classroom_by_uid(classroom_id)
    if user_id == classroom_obj.creator_uid:
        return True
    else:
        return False


def add_attendance_token_redis(classroom_uid, token, timeout = None):
    resp = attendance_redis.set_token(
        token, classroom_uid, timeout
    )
    return resp


def add_attendance_mongo(classroom_uid, token):
    resp = attendance_mongo.add_attendance_mongo(
        classroom_uid, token
    )
    return resp


def delete_attendance_token_redis(token):
    delete_token_rep = attendance_redis.delete_token(token)
    return delete_token_rep


def delete_attendance_mongo(classroom_uid, token):
    delete_resp = attendance_mongo.delete_attendance_mongo(
        classroom_uid, token
    )
    return delete_resp


def if_user_enrolled(classroom_uid, user_id):
    classroom_enrolled_resp = attendance_mongo.check_enrolled_in_classroom(classroom_uid, user_id)
    user_enrolled_resp = attendance_mongo.check_enrolled_in_user_enrolled(classroom_uid, user_id)

    # print('classroom_enrolled_resp: ', classroom_enrolled_resp)
    # print('user_enrolled_resp: ', user_enrolled_resp)

    if classroom_enrolled_resp ==  True and user_enrolled_resp == True:
        return True
    
    return False


def log_attendance(classroom_uid, user_id, attendance_token):
    ### check if token in redis
    valid = attendance_redis.get_token(attendance_token)
    print(valid)

    if valid:
        logged_attendance_resp = attendance_mongo.give_attendance(classroom_uid, user_id, attendance_token)

        if logged_attendance_resp ==  True:
            return True
    return False

