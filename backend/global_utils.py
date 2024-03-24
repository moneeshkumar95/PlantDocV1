from fastapi import status
import numpy as np


from datetime import datetime
from typing import Any
from io import BytesIO
from PIL import Image


from settings import AWS_KWARGS
from startup_shutdown_utils import create_s3_client, create_db_client, create_db_resource, load_model


CLASS_NAMES = ['tomato__bacterial spot',
               'tomato__early blight',
               'tomato__late blight',
               'tomato__leaf mold',
               'tomato__septoria leaf spot',
               'tomato__spider mites',
               'tomato__target spot',
               'tomato__yellow leaf curl virus',
               'tomato__mosaic virus',
               'tomato__healthy']


MODEL = load_model()

db_client = create_db_client(AWS_KWARGS)
db_resource = create_db_resource(AWS_KWARGS)
s3_client = create_s3_client(AWS_KWARGS)


def success_response(status_code=status.HTTP_200_OK, detail: str = '', data: Any = []):
    """
    For the success response
    :param status_code: status code
    :param detail: message
    :param data: data
    :return: response
    """
    response = {
        "status_code": status_code,
        "detail": detail,
        'data': data
    }
    return response

def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data))
    image = image.resize((256, 256))
    image = np.array(image)
    return image

def convert_to_lower(input_dict):
    return {key: value.lower() if isinstance(value, str) else value for key, value in input_dict.items() if value is not None}


def str_to_datetime(string):
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f")
