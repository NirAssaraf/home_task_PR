def create_pipeline(image_id,input_path,cv_tasks):
    return  [
            {
                '$match': {
                    '$or': [
                        {
                            'image_uniqueID': image_id
                        }, {
                            'input_path': input_path
                        }
                    ]
                }
            }, 
            {
                '$project': {
                    '_id': 0, 
                    'image': {
                        '$cond': [
                            {
                                '$eq': [
                                    '$image_uniqueID', image_id
                                ]
                            }, {
                                '$cond': [
                                    {
                                        '$eq': [
                                            '$input_path', input_path
                                        ]
                                    }, {
                                        'image_uniqueID': '$image_uniqueID', 
                                        'input_path': '$input_path', 
                                        'output_path': '$output_path', 
                                        'new_cv_tasks': {
                                            '$setDifference': [
                                               cv_tasks, '$cv_tasks'
                                            ]
                                        },
                                        "cv_tasks":"$cv_tasks" ,
                                        'error': 1
                                    }, {
                                        'error': 0
                                    }
                                ]
                            }, {
                                '$cond': [
                                    {
                                        'eq': [
                                            '$input_path',input_path
                                        ]
                                    }, {
                                        'image_uniqueID': '$image_uniqueID', 
                                        'input_path': '$input_path', 
                                        'output_path': '$output_path', 
                                        'cv_tasks': '$cv_tasks', 
                                        'error': 2
                                    }, 3
                                ]
                            }
                        ]
                    }
                }
            }
        ]


def images_helper(image) -> dict:
    return {
        "image_uniqueID": str(image["image_uniqueID"]),
        "input_path": image["input_path"],
        "output_path": image["output_path"],
        "cv_tasks": image["cv_tasks"]
    }