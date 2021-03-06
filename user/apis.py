from fastapi import BackgroundTasks, Depends, UploadFile, APIRouter, Body, Request
from starlette.responses import RedirectResponse
from tokens.controllers import token_validation
from fastapi.param_functions import File
from user import schemas as user_schemas
from user import routes as user_routes
from typing import Optional


router = APIRouter()


''' AUTH APIS '''

@router.post("/sign_up/", tags = ["user : auth"])
async def sign_up(user: user_schemas.UserSignUp, request: Request, bg: BackgroundTasks):
    #print(request.base_url)
    return await user_routes.sign_up(user, request.url_for("verify_user"), bg)


@router.post("/sign_in/", tags = ["user : auth"])
async def sign_in(user: user_schemas.UserSignIn):
    return await user_routes.sign_in(user)


@router.post("/sign_out/", tags = ["user : auth"])
async def sign_out(background_tasks: BackgroundTasks, token: dict = Depends(token_validation)):
    return await user_routes.sign_out(token, background_tasks)


''' ACCOUNT APIS '''

@router.post("/update_profile/", tags = ["users : account"])
async def update_profile(details: user_schemas.UpdateProfileSchema, token: dict = Depends(token_validation)):
    return await user_routes.update_profile(token, details)


@router.post("/update_password/", tags = ["users : account"])
async def update_password(details: user_schemas.UpdatePasswordSchema, token: dict = Depends(token_validation)):
    return await user_routes.update_password(token, details)


@router.post("/change_profile_picture/", tags = ["users : account"])
async def change_profile_picture(token: dict = Depends(token_validation), picture: Optional[UploadFile] = File(None)):
    return await user_routes.change_profile_picture(token, picture)


@router.post("/reset_password/", tags = ["users : account"])
async def reset_password(reset: user_schemas.ResetPasswordSchema):
    #print(reset.token, reset.email)
    return await user_routes.reset_password(reset)


@router.post("/delete_account/", tags = ["users : account"])
async def delete_account(password: user_schemas.DeleteUserSchema, bg: BackgroundTasks, token: dict = Depends(token_validation)):
    return await user_routes.delete_account(password, token, bg)


''' USER DATA APIS '''

@router.post('/get_user_dashboard/', tags = ["users : data"])
async def get_user_dashboard(token: dict = Depends(token_validation)):
    return await user_routes.get_user_dashboard(token)


@router.post("/get_username_from_user_id/", tags = ["users : data"])
async def get_username_from_user_id(user_uid: str = Body(..., embed=True), token: dict = Depends(token_validation)):
    return await user_routes.get_username_from_user_id(user_uid = user_uid, token = token)


@router.post("/get_any_user_profile/", tags = ["users : data"])
async def get_any_user_profile(username: str = Body(...), user_id: str = Body(...), token: dict = Depends(token_validation)):
    if username == '':
        return await user_routes.get_any_user_profile_from_user_id(user_id = user_id, token = token)
    else:
        return await user_routes.get_any_user_profile_from_username(username = username, token = token)
    

''' EMAIL APIS '''

@router.get("/verify_user/", tags = ["users : email"])
async def verify_user(token: str):
    #print(token)
    return await user_routes.verify_user(token)


@router.post("/send_reset_password/", tags = ["users : email"])
async def send_reset_password(request: Request, bg: BackgroundTasks, username: str = Body(..., embed = True), email: str = Body(..., embed = True)):
    return await user_routes.send_reset_password(username, email, "https://gs-suite.herokuapp.com/password/reset" , bg)