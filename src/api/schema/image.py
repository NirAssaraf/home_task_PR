from typing import List
from pydantic import BaseModel, Field


class ImagesSchema(BaseModel):
    image_uniqueID: int = Field(..., description="The unique ID of the image.")
    input_path: str = Field(..., description="The path of the input image.")
    output_path: str = Field(..., description="The path where the processed image will be saved.")
    cv_tasks: List[int] = Field(..., description="An array of integers representing the computer vision tasks associated with the image.")


    class Config:
        schema_extra = {
            'example': {
                "image_uniqueID" : 1,
                "input_path" : "/path/to/input/image.jpg",
                "output_path" : "/path/to/output/image.jpg",
                "cv_tasks" : [1, 2, 3]
            },
        }



def ErrorResponseModel(error, code, message):
    return {'error': error, 'code': code, 'message': message}
