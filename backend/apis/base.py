from fastapi import APIRouter


from .admin.router import admin_router
from .auth.router import auth_router
from .user.router import user_router
from .predict.router import predict_router

router = APIRouter(prefix="/api/v1")

# Including the User and task router
router.include_router(auth_router)
router.include_router(admin_router)
router.include_router(user_router)
router.include_router(predict_router)
