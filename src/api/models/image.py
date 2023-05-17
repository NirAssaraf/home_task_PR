import datetime
import os
import cv2

from utils.functions import create_pipeline
from db.database import images_collection
from utils.tasks import ComputerVisionTasks
from utils.functions import images_helper

class ImageModel:

    async def add_images(self,images):

        logs =[]

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        

        root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logs_directory = os.path.join(root_path, "files", "logs_files")
        
        # Create the logs directory if it doesn't exist
        os.makedirs(logs_directory, exist_ok=True)
        
        # Create the log file path
        log_file_path = os.path.join(logs_directory, f"log_{timestamp}.txt")

        for item in images:
            image = images_helper(item)

            unique_id = image["image_uniqueID"]
            input_path = image["input_path"]
            cv_tasks = image["cv_tasks"]
            output_path = image["output_path"]

            pipeline = create_pipeline(unique_id,input_path,cv_tasks)

            data = await images_collection.aggregate(pipeline).to_list(None)
            for result in data:
                image_from_db = result["image"]
                if image_from_db:
                    if image_from_db["error"] == 0:
                        timestamp = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
                        logs.append(f"[{timestamp}]:Error - Same uniqueID for an image with a different file location - do not perform the computer vision tasks in this case.")
                        continue
                    elif image_from_db["error"] == 1:
                        timestamp = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
                        logs.append(f"[{timestamp}]:Warning - Same uniqueID and same file location, with a different list of computer vision tasks")
                        await self.execute(image_from_db["input_path"],image_from_db["output_path"],image_from_db["new_cv_tasks"])
                        image["cv_tasks"] = image_from_db["cv_tasks"] + image_from_db["new_cv_tasks"]
                        await images_collection.update_one(
                        {"image_uniqueID": unique_id},
                        {"$set": image},
                        upsert=False)                    
                        continue
                    elif image_from_db["error"] == 2:
                        timestamp = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
                        logs.append(f"[{timestamp}]:Warning - Same file location with different uniqueID")
                        await self.execute(image["input_path"],image["output_path"],image["cv_tasks"])
                        continue      
            if not data:          
                await images_collection.update_one(
                {"image_uniqueID": unique_id},
                {"$set": image},
                upsert=True)
                timestamp = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
                logs.append(f"[{timestamp}]:success")
                await self.execute(input_path,output_path,cv_tasks)
            
        # Write logs to the log file
        with open(log_file_path, "a") as f:
            for log in logs:
                f.write(f"{log}\n")

        return  f"{log_file_path}"
    

    async def execute(self,input_path,output_path,cv_task_list):
        cv_tasks = ComputerVisionTasks()
        image = cv2.imread(input_path)
        
        # Perform computer vision tasks based on cv_task_list
        for cv_task in cv_task_list:
            if cv_task == 1:
                image = cv_tasks.rotate_image(image)
            elif cv_task == 2:
                image = cv_tasks.dilate_image(image)
            elif cv_task == 3:
                image = cv_tasks.erode_image(image)
            elif cv_task == 4:
                image = cv_tasks.perform_canny_edge_detection(image)
            elif cv_task == 5:
                image = cv_tasks.resize_image(image)

        # Update the existing image if output_path exists

        if os.path.exists(output_path):
            output_image = cv2.imread(output_path)
            output_image = image
            cv2.imwrite(output_path, output_image)
        else:
            # Save the processed image to output_path
            cv2.imwrite(output_path, image)

 
    async def get_image(self,id: str) -> dict:
        image = await images_collection.find_one({'image_uniqueID': id})
        if image:
            return images_helper(image)
        return {}
    
    async def get_images(self):
        images = await images_collection.find({}).to_list(None)
        if images:
            return [images_helper(image) for image in images]
        return []

 

    async def delete_image(self,id: str):
        image = await images_collection.find_one({'image_uniqueID':id })
        if image:
            await images_collection.delete_one({'image_uniqueID':id })
            return True
        return False
