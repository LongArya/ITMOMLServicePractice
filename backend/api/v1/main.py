from fastapi import APIRouter

from backend.api.v1.routes import user, auth, prediction

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(prediction.router, prefix="/prediction", tags=["prediction"])
