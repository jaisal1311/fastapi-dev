from tokens.controllers import token_validation
from fastapi.param_functions import Depends

from announcements import routes as announcement_routes

from fastapi import Body, APIRouter, BackgroundTasks


router = APIRouter()


@router.post('/create_announcement_pane/')
async def create_annonuncement_pane(classroom_uid: str = Body(..., embed=True), token: dict = Depends(token_validation)):
    return await announcement_routes.create_announcement_pane(classroom_uid, token)


@router.post('/post_announcement/')
async def post_announcement(background_tasks: BackgroundTasks, classroom_uid: str = Body(...), announcement: str = Body(...), token: dict = Depends(token_validation)):
    return await announcement_routes.post_announcement(classroom_uid, announcement, background_tasks, token)


@router.post('/get_all_announcements/')
async def get_all_announcements(classroom_uid: str = Body(..., embed=True), token: dict = Depends(token_validation)):
    return await announcement_routes.get_all_announcements(classroom_uid, token)


@router.post('/delete_announcement/')
async def delete_announcement(token: dict = Depends(token_validation), classroom_uid: str = Body(...), announcement_id: str = Body(...)):
    return await announcement_routes.delete_announcement(classroom_uid = classroom_uid, announcement_id = announcement_id, token = token)