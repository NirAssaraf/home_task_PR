from fastapi import APIRouter
from fastapi import HTTPException
from api.controllers.image import ImageController

class ImageRouter():
    def __init__(self):
        self.router = APIRouter()
        self.image_controller = ImageController()

    def include_routes(self):
        self.router.post('/', response_description='Image data added into the database')(self.add_images)
        self.router.get('/', response_description="Images retrieved")(self.get_images)
        self.router.get('/{id}', response_description="Image data retrieved")(self.get_image)
        self.router.delete('/{id}', response_description="Image data deleted from the database")(self.delete_image)

    async def add_images(self, data: dict):
        try:
            return await self.image_controller.add_images(data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
        
    async def get_images(self):
        return await self.image_controller.get_images()

    async def get_image(self, id):
        return await self.image_controller.get_image(id)


    async def delete_image(self, id: str):
        return await self.image_controller.delete_image(id)
    
    def get_router(self):
        return self.router
