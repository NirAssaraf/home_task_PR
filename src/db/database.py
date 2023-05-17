import os

import motor.motor_asyncio
from decouple import config
from utils.tasks import ComputerVisionTasks 
from  api.schema.image import ImagesSchema


try:
    MONGO_DETAILS = config('MONGO_DETAILS')
except:
    MONGO_DETAILS = os.getenv('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.images

images_collection = database.get_collection('images_collection')

