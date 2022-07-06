from typing import List

from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from synopsis.data.models.users import User, UserIn, Users
from synopsis.data.primitives import Status

router: APIRouter = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[User])
async def get_users():
    return await User.from_queryset(Users.all())


@router.post("/", response_model=User)
async def create_user(user: UserIn):
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User.from_tortoise_orm(user_obj)


@router.get("/user/{user_id}", response_model=User, responses={404: {"model": HTTPNotFoundError}})
async def get_user(user_id: int):
    return await User.from_queryset_single(Users.get(id=user_id))


@router.put("/user/{user_id}", response_model=User, responses={404: {"model": HTTPNotFoundError}})
async def update_user(user_id: int, user: UserIn):
    await Users.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User.from_queryset_single(Users.get(id=user_id))


@router.delete("/user/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")
