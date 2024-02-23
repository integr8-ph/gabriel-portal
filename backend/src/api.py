from fastapi import APIRouter

from src.users import routes


router = APIRouter()

router.include_router(routes.router)
