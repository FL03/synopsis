from typing import List

from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from synopsis.data.models.items import Items, Item, ItemIn
from synopsis.data.primitives import Status

router: APIRouter = APIRouter(prefix="/item", tags=["item"])
std_responses = {"404": dict(model=HTTPNotFoundError)}


@router.get("/", response_model=List[Item])
async def get_items():
    return await Item.from_queryset(Items.all())


@router.post("/", response_model=Item)
async def create_item(item: ItemIn):
    obj = await Items.create(**item.dict(exclude_unset=True))
    return await Item.from_tortoise_orm(obj)


@router.get("/item/{oid}", response_model=Item, responses=std_responses)
async def get_item(oid: int):
    return await Item.from_queryset_single(Items.get(id=oid))


@router.put("/item/{oid}", response_model=Item, responses=std_responses)
async def update_item(oid: int, account: ItemIn):
    await Items.filter(id=oid).update(**account.dict(exclude_unset=True))
    return await Item.from_queryset_single(Items.get(id=oid))


@router.delete("/item/{oid}", response_model=Status, responses=std_responses)
async def delete_item(oid: int):
    deleted_count = await Items.filter(id=oid).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Item {oid} not found")
    return Status(message=f"Deleted item {oid}")
