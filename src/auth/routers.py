import json
from typing import Annotated

from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

from pydantic import EmailStr

from src.auth.repository import UsersRepository, RefreshSessionsRepository
from src.auth.schemas import SUserRegister, SUser
from src.auth.utils import generate_url_token , decode_url_token, send_confirmation_email, send_password_reset_email
from src.auth.auth import generate_password_hash, verify_passwords, generate_jwt_token, decode_jwt_token

from datetime import datetime, timezone

REFRESH_TOKEN_EXPIRE_DAYS = 30

router = APIRouter(
    prefix="/auth",
    tags=["Authentification"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register")
async def register_user(user_data:SUserRegister) -> str:
    user_as_dict= user_data.model_dump(exclude={"password2"})

    password = generate_password_hash(user_as_dict["password"])
    user_as_dict["password"] = password
    user_id = await UsersRepository.add_one(user_as_dict)
    timestamp = datetime.now(timezone.utc).strftime("%m/%d/%Y")

    user_payload = {
        "user_id":user_id,
        "timestamp": timestamp
    }
    user_json = json.dumps(user_payload)
    token = generate_url_token(user_json)

    send_confirmation_email(user_as_dict["email"], token)

    return token

@router.get("/confirm")
async def user_activation(token:str) -> SUser:
    print(token)
    token_data = decode_url_token(token)
    user = await UsersRepository.activate_user(token_data["user_id"])
    if user:
        return user
    
    raise HTTPException(
        status_code=500,
        detail="Не удалось активировать учетную запись"
    )

@router.post("/login")
async def login(response: Response, user_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await UsersRepository.get_user(username=user_data.username)
    print(user)
    if user:
        if not user.active:
            raise HTTPException(
            status_code=400,
            detail="User is not active"
            )
        if verify_passwords(user_data.password, user.password):
            user_payload = {
                "user_id":user.id,
                "username":user.username
            } # add user role in future
            access_token = generate_jwt_token(user_payload)
            refresh_token = await RefreshSessionsRepository.create(user.id)
            

            response.set_cookie(
                key = "access_token",
                value = access_token,
                path = "/",
            )

            response.set_cookie(
                key = "refresh_token",
                value = refresh_token,
                max_age = 60 * 60 * 24 * REFRESH_TOKEN_EXPIRE_DAYS,
                path = "/",
                httponly = True
            )
            return {"access_token": access_token,  "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=401,
                detail="Wrong email or password"
            )
    raise HTTPException(
            status_code=400,
            detail="User with this data does not exists"
        )

async def get_current_user(access_token:Annotated[str,Depends(oauth2_scheme)]) -> SUser:
    print(access_token)
    user_data = decode_jwt_token(access_token)
    user = await UsersRepository.get_user(id=user_data["user_id"])
    if user:
        return user
    return HTTPException(
            status_code=400,
            detail="User with this data does not exists"
        )

async def get_active_user(user:Annotated[SUser, Depends(get_current_user)]) -> SUser:
    print(user)
    if not user.active:
        raise HTTPException(
            status_code=400,
            detail="User is not active"
        )
    return user

#just fo test use request header
@router.get("/users/me")
async def get_me(current_user:Annotated[SUser, Depends(get_active_user)]):
    return current_user
    

@router.post("/refresh")
async def refresh_token(request: Request, response: Response, user:Annotated[SUser,Depends(get_active_user)]):
    print(request.cookies)
    refresh = request.cookies["refresh_token"]
    await RefreshSessionsRepository.delete(refresh)
    new_refresh_session = await RefreshSessionsRepository.create(user.id)
    user_payload = {
                "user_id":user.id,
                "username":user.username
            }
    new_access_token = generate_jwt_token(user_payload)

    response.set_cookie(
        key = "access_token",
        value = new_access_token,
        path = "/",
    )

    response.set_cookie(
        key = "refresh_token",
        value = new_refresh_session,
        max_age = 60 * 60 * 24 * REFRESH_TOKEN_EXPIRE_DAYS,
        path = "/",
        httponly = True
    )

    return {"access_token": new_access_token, "token_type":"bearer"}

#use get_active_user instead request
@router.post("/logout")
async def logout(request: Request,response: Response):
    refresh = request.cookies["refresh_token"]
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    await RefreshSessionsRepository.delete(refresh)

    return {"msg": "Successful logout"}


@router.post("/password/reset/request")
async def reset_password(email:EmailStr):
    user = await UsersRepository.get_user(email=email)

    if user:
        timestamp = datetime.now(timezone.utc).strftime("%m/%d/%Y")
        user_payload = {
            "user_id":user.id,
            "timestamp": timestamp
        }
        user_json = json.dumps(user_payload)
        token = generate_url_token(user_json)

        send_password_reset_email(user.email, token)

        return {"msg": "Password reset email sent"}

    else:
        raise HTTPException(
            status_code = 404,
            detail = "User with this email does not exists"
        )

@router.post("/password/reset/confirm")
async def password_reset_confirm(token: str, password1: str, password2: str):
    if password1 != password2:
        raise HTTPException(
            status_code=500,
            detail="Passwords does not matching"
        )

    token_data = decode_url_token(token)
    print(token_data)
    password_hash = generate_password_hash(password1)
    await UsersRepository.change_password(user_id=token_data["user_id"], password=password_hash)

    return {"msg": "Password reset successful"}

@router.post("/password/change")
async def change_password(
    old_password:str,
    password1:str,
    password2:str,
    user: Annotated[SUser, Depends(get_active_user)]
):
    if password1 != password2:
        raise HTTPException(
            status_code=500,
            detail="Passwords does not matching"
        )
    
    if verify_passwords(old_password, user.password):
        await UsersRepository.change_password(user.id, generate_password_hash(password1))
        await RefreshSessionsRepository.clear_all_sessions_for_user(user.id)
        return {"msg": "Password changed successfully"}

    raise HTTPException(
        status_code=500,
        detail="Old and current password does not matching"
    )