from fastapi import APIRouter


from synopsis.data.models.items import Items, Item, ItemIn

router: APIRouter = APIRouter(prefix="/item", tags=["item"])


@router.get("/")
async def items() -> dict:
    return dict(data=[])


@router.delete("/{pid}")
async def delete_item(cid: str) -> dict:
    return dict(id=cid)


@router.get("/{pid}")
async def get_item(cid: str) -> dict:
    return dict(id=cid)


@router.post("/{cid}")
async def post_item(cid: str) -> dict:
    return dict(id=cid)


@router.put("/{pid}")
async def put_item(cid: str) -> dict:
    return dict(id=cid)
