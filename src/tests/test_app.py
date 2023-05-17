import pytest
import sys
import os
import cv2

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from fastapi.testclient import TestClient
from src.app import app
from src.api.routes.image import ImageRouter
from src.api.controllers.image import ImageController
from src.api.models.image import ImageModel

client = TestClient(app)


def test_read_main():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'App is running!'}


def test_read_images_list():
    response = client.get('/api/image/')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_images():
    data = {
        "images": [
            {
                "image_uniqueID": 1,
                "input_path": "src/files/input/pan1D.jpg",
                "output_path": "src/files/output/pan1D.jpg",
                "cv_tasks": [1, 2, 3]
            }
        ]
    }
    response = client.post('/api/image', json=data)
    assert response.status_code == 200
    response_data = response.json()
    log_file_path = response_data["log_file_path"]

    assert os.path.exists(log_file_path)

    with open(log_file_path, "r") as f:
        logs = f.readlines()

    assert len(logs) == 1
    os.remove(log_file_path)


@pytest.mark.asyncio
async def test_get_images():
    # add some images to the database
    data = {
        "images": [
            {
                "image_uniqueID": 2,
                "input_path": "src/files/input/pan2D.jpg",
                "output_path": "src/files/output/pan2D.jpg",
                "cv_tasks": [1, 2, 3]
            },
            {
                "image_uniqueID": 3,
                "input_path": "src/files/input/pan3D.jpg",
                "output_path": "src/files/output/pan3D.jpg",
                "cv_tasks": [2, 3]
            }
        ]
    }
    await client.post('/api/image', json=data)

    # retrieve all images from the database
    response = await client.get('/api/image/')
    assert response.status_code == 200

    # check that the response contains the added images
    response_data = response.json()
    assert len(response_data) == 2
    assert response_data[0]["image_uniqueID"] == 2
    assert response_data[1]["image_uniqueID"] == 3

    # cleanup
    for image in response_data:
        await client.delete(f'/api/image/{image["id"]}')


@pytest.mark.asyncio
async def test_get_image():
    # add an image to the database
    data = {
        "images": [
            {
                "image_uniqueID": 4,
                "input_path": "src/files/input/pan4D.jpg",
                "output_path": "src/files/output/pan4D.jpg",
                "cv_tasks": [1]
            }
        ]
    }
    response = await client.post('/api/image', json=data)
    response_data = response.json()
    image_id = response_data["images"][0]["id"]

    # retrieve the image by ID
    response = await client.get(f'/api/image/{image_id}')
    assert response.status_code == 200

    # check that the retrieved image is the same as the added image
    response_data = response.json()
    assert response_data["image_uniqueID"] == 4
    await client.delete(f'/api/image/{image_id}')
@pytest.mark.asyncio
async def test_delete_image():
    # add an image to the database
    data = {
        "images": [
        {
            "image_uniqueID": 5,
            "input_path": "src/files/input/pan5D.jpg",
            "output_path": "src/files/output/pan5D.jpg",
            "cv_tasks": [1]
        }
        ]
    }
    response = await client.post('/api/image', json=data)
    response_data = response.json()
    image_id = response_data["images"][0]["id"]
    # delete the image
    response = await client.delete(f'/api/image/{image_id}')
    assert response.status_code == 200

    # try to retrieve the deleted image
    response = await client.get(f'/api/image/{image_id}')
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_invalid_image_data():
# try to add an image with missing required fields
    invalid_data = {
    "images": [
        {
            "input_path": "src/files/input/pan6D.jpg",
            "output_path": "src/files/output/pan6D.jpg",
            "cv_tasks": [1]
        }
    ]
    }
    response = await client.post('/api/image', json=invalid_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_nonexistent_image():
    response = await client.get('/api/image/none-existent')
    assert response.status_code == 404