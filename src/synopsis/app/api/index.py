from fastapi import APIRouter

from .endpoints import item, profile, timeslip, users

router: APIRouter = APIRouter(prefix="/api", tags=["default"])


@router.post("/token")
async def token_post() -> dict:
    return dict(token="some_token")

router.include_router(router=item.router)
router.include_router(router=profile.router)
router.include_router(router=timeslip.router)
router.include_router(router=users.router)
