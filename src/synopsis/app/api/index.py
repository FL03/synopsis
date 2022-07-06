from fastapi import APIRouter, Depends

from .endpoints import item, oauth, profile, timeslip, users

router: APIRouter = APIRouter(prefix="/api", tags=["default"])

router.include_router(router=item.router, dependencies=[Depends(oauth.get_current_active_user)])
router.include_router(router=oauth.router)
router.include_router(router=profile.router, dependencies=[Depends(oauth.get_current_active_user)])
router.include_router(router=timeslip.router, dependencies=[Depends(oauth.get_current_active_user)])
router.include_router(router=users.router)
