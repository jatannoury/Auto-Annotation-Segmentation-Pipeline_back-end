import base64
import datetime
from typing import List, Dict

import numpy as np
from PIL import Image
import io
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
import cv2
from fastapi.responses import JSONResponse

from tools.openCV_tool import random_bounding_box

router = APIRouter()

@router.post("/single", status_code=201)
async def upload_image(file:bytes= File(...)):
    allowed_extensions = [".jpeg", ".png", ".jpg",".avif"]
    image = Image.open(io.BytesIO(file))
    image = np.array(image)  # Convert PIL Image to numpy array
    image_with_bbox = random_bounding_box(image)
    for extension in allowed_extensions:
        try:
            _, buffer = cv2.imencode(extension, cv2.cvtColor(image_with_bbox, cv2.COLOR_RGB2BGR))
        except:
            continue

    # Encode the bytes as base64
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    return JSONResponse(content={"uploadStatus": "complete", "image": image_base64},status_code=201)


@router.post("/batch", status_code=201)
async def upload_multiple_images(file_uploads: List[UploadFile]):
    allowed_extensions = [".jpeg", ".png", ".jpg", ".avif"]
    response = []
    for file in file_uploads:
        file = await file.read()
        image = Image.open(io.BytesIO(file))
        image = np.array(image)  # Convert PIL Image to numpy array
        image_with_bbox = random_bounding_box(image)
        for extension in allowed_extensions:
            try:
                _, buffer = cv2.imencode(extension, cv2.cvtColor(image_with_bbox, cv2.COLOR_RGB2BGR))
            except:
                continue

        # Encode the bytes as base64
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        response.append(image_base64)
    return JSONResponse(content={"uploadStatus": "complete", "images": response}, status_code=201)
