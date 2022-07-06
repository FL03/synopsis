from typing import List

from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from synopsis.data.models.users import Account, AccountIn, Accounts
from synopsis.data.primitives import Status

router: APIRouter = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/", response_model=List[Account])
async def get_profiles():
    return await Account.from_queryset(Accounts.all())


@router.post("/", response_model=Account)
async def create_profile(user: AccountIn):
    user_obj = await Accounts.create(**user.dict(exclude_unset=True))
    return await Account.from_tortoise_orm(user_obj)


@router.get("/profile/{uid}", response_model=Account, responses={404: {"model": HTTPNotFoundError}})
async def get_profile(uid: int):
    return await Account.from_queryset_single(Accounts.get(id=uid))


@router.put("/profile/{uid}", response_model=Account, responses={404: {"model": HTTPNotFoundError}})
async def update_profile(uid: int, account: AccountIn):
    await Accounts.filter(id=uid).update(**account.dict(exclude_unset=True))
    return await Account.from_queryset_single(Accounts.get(id=uid))


@router.delete("/profile/{uid}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(uid: int):
    deleted_count = await Accounts.filter(id=uid).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Account {uid} not found")
    return Status(message=f"Deleted account {uid}")



