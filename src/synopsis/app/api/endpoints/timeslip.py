from fastapi import APIRouter
from typing import List
from synopsis.data.models.users import Slips, Slip, SlipIn

from tortoise.contrib.fastapi import HTTPNotFoundError

router: APIRouter = APIRouter(prefix="/slips", tags=["slips"])


@router.get("/", response_model=List[Slip])
async def get_slips():
    return await Slip.from_queryset(Slips.all())


@router.post("/", response_model=Slip)
async def add_slip(slip: SlipIn):
    slip_obj = await Slips.create(**slip.dict(exclude_unset=True))
    return await Slip.from_tortoise_orm(slip_obj)


@router.delete("/{sid}", response_model=List[Slip], responses={404: {"model": HTTPNotFoundError}})
async def delete_slip(sid: str):
    return dict(id=sid)


@router.get("/{sid}", response_model=List[Slip])
async def get_slip(sid: str):
    return dict(id=sid)


@router.put("/{sid}", response_model=List[Slip])
async def update_slip(sid: str) -> dict:
    return dict(id=sid)
