from fastapi import APIRouter

from backend.api.v1.routes import user, auth

api_router = APIRouter()
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
