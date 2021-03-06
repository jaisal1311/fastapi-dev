from responses.not_owner_response_body import NotOwnerResponseBody
from responses.standard_response_body import StandardResponseBody
from classrooms import controllers as classroom_controllers
from classrooms import models as classroom_models
from forum import controllers as forum_controllers
from user import controllers as user_controllers
from forum import helpers as forum_helpers
from forum import mongo as forum_mongo
import datetime


async def create_forum(classroom_uid, token):

    classroom_exist_status = await classroom_models.get_classroom_by_uid(uid = classroom_uid)
    if not classroom_exist_status:
        return StandardResponseBody(
            False, 'Create classroom before creating forum', token.token_value
        )

    if_user_creator = await classroom_controllers.check_user_if_creator(classroom_id=classroom_uid, user_id=token.user_id)

    if if_user_creator == True:
        if_forum_exists = await forum_mongo.check_if_forum_exists(classroom_uid)

        if if_forum_exists['forum_exists'] == True:
            return StandardResponseBody(
                False, 'Forum already exists', token.token_value
            )
        else:
            forum_creation_status = await forum_controllers.create_forum(classroom_uid)
            if forum_creation_status == True:
                return StandardResponseBody(
                    True, 'Forum has been created', token.token_value
                )
            else:
                return StandardResponseBody(
                    True, 'Forum could not be created', token.token_value
                )
    else:
        return NotOwnerResponseBody(token.token_value)
        

async def get_forum_chat(classroom_uid, token):
    user_enrolled_status = await classroom_controllers.if_user_enrolled(classroom_uid=classroom_uid, user_id=token.user_id)
    if_user_is_creator = await classroom_controllers.check_user_if_creator(classroom_id=classroom_uid, user_id=token.user_id)

    if user_enrolled_status or if_user_is_creator:
        if_forum_exists = await forum_mongo.check_if_forum_exists(classroom_uid=classroom_uid)

        if if_forum_exists['forum_exists'] == True:
            get_all_messages_response_dict = await forum_controllers.get_all_messages(classroom_uid = classroom_uid)

            if 'status' in get_all_messages_response_dict.keys():
                '''if status exists then mongo failed'''
                return StandardResponseBody(
                    get_all_messages_response_dict['status'], get_all_messages_response_dict['message'], token.token_value
                )
            else:
                return StandardResponseBody(
                    True, 'Forum messages have been acquired', token.token_value, {'forum_stuff': get_all_messages_response_dict}
                )
        
        else:
            return StandardResponseBody(
                False, 'Forum does not exist', token.token_value
            )
    else:
        return StandardResponseBody(
            False, 'You are not part of this classroom', token.token_value
        ) 


async def send_message(classroom_uid, message, reply_user_id, reply_msg_id, tkn):
    reply_user_id_username = ''

    user_enrolled_status = await classroom_controllers.if_user_enrolled(classroom_uid=classroom_uid, user_id=tkn.user_id)
    if_user_is_creator = await classroom_controllers.check_user_if_creator(classroom_id=classroom_uid, user_id=tkn.user_id)
    
    '''For reply id'''
    if reply_user_id != '':
        reply_user_id_enrolled_status = await classroom_controllers.if_user_enrolled(classroom_uid=classroom_uid, user_id=reply_user_id)
        reply_user_id_creator_status = await classroom_controllers.check_user_if_creator(classroom_id=classroom_uid, user_id=reply_user_id)

        if reply_user_id_enrolled_status or reply_user_id_creator_status:
            reply_user_id_username = await user_controllers.get_user_username(uid=reply_user_id)

        else:
            return StandardResponseBody(
                False, 'You cannot reply to mentioned user', tkn.token_value
            )

    
    if user_enrolled_status or if_user_is_creator:

        '''Check if forum exists'''
        if_forum_exists = await forum_mongo.check_if_forum_exists(classroom_uid=classroom_uid)

        if if_forum_exists['forum_exists'] == True:

            ''' to get username '''
            username = await user_controllers.get_user_username(uid=tkn.user_id)
            
            message_id = await forum_helpers.generate_message_code()

            send_message_status = await forum_controllers.send_message(
                classroom_id=classroom_uid,
                message_id = message_id,
                reply_user_id = reply_user_id,
                reply_username = reply_user_id_username,
                reply_msg_id = reply_msg_id,
                datetimestamp = datetime.datetime.now(),
                user_id = tkn.user_id,
                username = username,
                message = message
            )

            if send_message_status ==  True:
                return StandardResponseBody(
                    True, 'Message has been posted to forum', tkn.token_value, {'message_id': message_id}
                )
            else:
                return StandardResponseBody(
                        False, 'Message could not be posted to forum', tkn.token_value
                    )
        else:
            return StandardResponseBody(
                False, 'Forum has not been created', tkn.token_value
            )  
    else:
        return StandardResponseBody(
            False, 'You cannot send messsages to this forum', tkn.token_value
        )
            

async def delete_forum(classroom_uid, token):
    classroom_exist_status = await classroom_models.get_classroom_by_uid(uid = classroom_uid)
    if not classroom_exist_status:
        return StandardResponseBody(False, 'Classroom does not exist', token.token_value)

    if_user_creator = await classroom_controllers.check_user_if_creator(classroom_id=classroom_uid, user_id=token.user_id)
    if if_user_creator:
        
        if_forum_exists = await forum_mongo.check_if_forum_exists(classroom_uid)
        if if_forum_exists['forum_exists'] != True:
            return StandardResponseBody(False, 'Forum does not exist', token.token_value)
        else:
            forum_deletion_status = await forum_controllers.delete_forum(classroom_uid)
            if forum_deletion_status:
                return StandardResponseBody(True, 'Forum has been deleted', token.token_value)
            else:
                return StandardResponseBody(True, 'Forum could not be deleted', token.token_value)
    else:
        return NotOwnerResponseBody(token.token_value)
        