# Home Task - Pashot Robotic

In this project i designed and implemented a system that receives json files, each consisting of a list
of images (uniqueID + file location) and a list of computer vision tasks to perform on every
image.


Project structure:
```
.
├── README.md
├── src
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── routes
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── image.py
│   │   ├── controller
│   │   │   ├── __init__.py
│   │   │   └── image.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── image.py
│   │   └── schema
│   │   │   ├── __init__.py
│   │   │   └── image.py
│   ├── db
│   │    ├── database.py
│   │    └── docker-compose.py
│   ├── files
│   │    ├── input
│   │    ├── logs_files
│   │    └── output
│   │
│   ├── tests
│   │    ├── __init__.py
│   │    └── test_app.py
│   │
│   ├── utils
│   │    ├── functions.py
│   │    └── tasks.py
│   │
│   ├── app.py
│   │
│   └── main.py
│   
└── requirements.txt
```

* src - holds all projects code
* api.routes - holds router base class and all the routers (the endpoints of the serve) 
* api.controllers - holds all controllers, the controler gets the data from the request and handle errors 
* api.model - holds all models, the model gets the data from the controller and by connecting to db gets the info by pipeline
* db - in this folder you will find the connection to the db and a docker-compose file to upload container of mongoDB
* files - this folder contains local input images, local output images after performed and folder of logs files
* utils - this folder has 2 files, the first (functions) is for function that used in the project but generic, the second is the task, is contains a class to perfom the computer vision tasks.


## Running 

1. pip install requirements.txt
2. Run following command:
    1. from the '/src/db' - docker compose up
3. Start server by running "py main.py"

## Endpoints

POST http://127.0.0.1:3000/api/image

REQUEST
```json
{
	"images": [
        {
            "image_uniqueID" : 1,
            "input_path" : "files/input/pan1A.jpg",
            "output_path" : "files/output/pan1A.jpg",
            "cv_tasks" : [1, 2, 3]
        }
    ]
}
```
RESPONSE
```json
{
    "log_file_path": "C:\\Users\\yariv\\Desktop\\Nir\\Python\\crud-fastapi-mongodb-main\\src\\files\\logs_files\\log_2023-05-17_20-33-04.txt"

}
```
Get http://127.0.0.1:3000/api/image

RESPONSE
```json
[
    {
        "image_uniqueID": "1",
        "input_path": "files/input/pan1A.jpg",
        "output_path": "files/input/pan1A.jpg",
        "cv_tasks": [
            1,
            2,
            3
        ]
    },
    {
        "image_uniqueID": "2",
        "input_path": "files/input/pan2A.jpg",
        "output_path": "files/input/pan2A.jpg",
        "cv_tasks": [
            1,
            2,
            3
        ]
    }
]
```
Get http://127.0.0.1:3000/api/image/1

RESPONSE
```json
{
    "image_uniqueID": "1",
    "input_path": "files/input/pan1A.jpg",
    "output_path": "files/input/pan1A.jpg",
    "cv_tasks": [
        1,
        2,
        3
    ]
}
```
DELETE http://127.0.0.1:3000/api/image/1

RESPONSE
```
    "Image with ID: 1 removed, Image deleted successfully"
```