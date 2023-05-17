from fastapi import HTTPException
from api.schema.image import ErrorResponseModel
from api.models.image import ImageModel
import os
class ImageController:
    def __init__(self):
        self.model = ImageModel()

    async def add_images(self,data: dict):
        try:
            images = data.get("images", [])
            log_file = await self.model.add_images(images)
            current_directory = os.getcwd()
            file_path = os.path.join(current_directory, log_file)
            return  {"log_file_path": file_path}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    async def get_images(self):
        images = await self.model.get_images()
        if images:
            return images
        return []


    async def get_image(self,id):
        image = await self.model.get_image(id)
        if image:
            return image
        return ErrorResponseModel('An error occurred', 404, 'Image doesn\'t exist.')

    async def delete_image(self,id: str):
        deleted_image = await self.model.delete_image(id)
        if deleted_image:
            return f"Image with ID: {id} removed, Image deleted successfully"
        return ErrorResponseModel(
            "An error occurred", 404, f"Image with id {id} doesn't exist"
        )
