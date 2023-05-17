from fastapi import APIRouter
from api.routes.image import ImageRouter

class BaseRouter:
    def __init__(self):
        self.router = APIRouter()
        self.image_router = ImageRouter()
        self.image_router.include_routes()

    def include_routes(self):
        self.router.include_router(self.image_router.get_router(), tags=['Image'], prefix='/image')

    def get_router(self):
        return self.router
